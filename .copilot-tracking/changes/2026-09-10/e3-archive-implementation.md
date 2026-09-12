---
title: E3 archive implementation evidence
description: Fixed-record codec research, implementation scope, and conformance evidence
ms.date: 2026-09-10
---

## Status and scope

Complete for the implemented component scope, not for a complete archive system.
This is the task's research and implementation note, kept at the
authorized changes path rather than creating a separate research artifact.
Only e3/archive.py, test_e3_archive.py, and this note are owned by this task.

## Questions and verified evidence

* The initial `python -B verify_e3_design.py` passed all 23 files, with no failures.
* E3_INTERFACE_CONTRACT_v0_9.md was read in full, including all archive layouts.
  The 512-byte summary has a 16-byte header and 62 unsigned 64-bit counters.
  There is no floating-point field or NaN/absence convention in that record.
* E3_INTEGRATION_DECISION_v0_11.md was read in full. Combined ordinal limits,
  SCRIPTED product 13, policies 5/6, namespace 34, and G IDs 400..403 apply.
* E3_CONFORMANCE_CONTRACT_v0_10.md was read in full. Script/oracle diagnostics
  do not authorize final targets or certify ordinary execution/replay.
* Existing e3/protocol.py demonstrates closed frozen records, strict built-in
  integers, immutable bytes, and rejection of reserved catalog slots.
* The workspace has no Git repository. All three authorized output paths were
  absent before this task; no preexisting workspace file was changed by this task.
* E3_EVALUATION_CONTRACT_v0_8.md, service-count paragraph, fixes core planned
  outer services at 3,311,370,832. Combined v0.11 count is 3,320,673,872.
* E3_POLICY_CONTRACT_v0_5.md, "Fixed-drive diagnostic with a different objective",
  defines scrub return 16 and resource return zero for DRIVE. A capsule does not
  contain G objective. Main-objective equality must therefore be contextual,
  not an unconditional codec check. An explicit regression fixture covers both.

## Implementation and validation

Implemented in e3/archive.py with standard-library dependencies only:

| Record | Bytes | Scope |
|--------|-------|-------|
| ResponseRecord | 8 | Every frozen response field, signed b and presence bits |
| TickCapsule / TickRecord | 16 / 48 | Exact packed fields and full-state SHA256 |
| SnapshotRecord | 308 | Dense header and untouched 276-byte payload |
| ResetAuditRecord | 64 | Source links, lifecycle, asserted checks and source digest |
| LessonRecord / CommitRecord | 8 / 4 | Exact statuses, V/A/W and staging fields |
| TemplateRecord | 64 | Exact fields, stock vectors and scalar presence |
| SummaryRecord | 512 | Header plus all 62 uint64 counters in frozen order |
| PrimitiveEvent | 192 | Fixed header, quotes/flows, raw fields and scratch |
| DirectoryEntry | 72 | Global ranges, widths, offsets, lengths and SHA256 |
| TraceCommitment | 48 | Event/scalar counts and whole-phase digest |
| ScheduleRecord | 1312 | Exact header, low-first cue nibbles, zero unused tail |
| PhaseDescriptor / ClassMapping | 64 / 32 | Exact catalog layouts and combined limits |
| GRecord | 128 | Frozen grid, underlying RL for FROZEN, script IDs 400..403 |
| Stocks / SummaryCounters | 6 / 496 | Typed immutable nested values |

`marshal` and `unmarshal` accept a closed record union and immutable bytes.
Re-encoding checks every reserved field and unused schedule nibble. Construction
and encoding reject bools as integers, out-of-range fields, mutable payloads,
custom record subclasses and malformed enum values. All-ones references map to
`None`; zero remains a valid row. No float is accepted in the binary records.
An IEEE NaN bit pattern in a summary is an ordinary uint64 integer, not NaN.

Reference helpers check global ranges, actual table extents, missing finalized
payloads, matching offsets/bytes and physical bounds without allocating tables.
`CORE_COUNTS`, `EXTENSION_COUNTS` and `COMBINED_COUNTS` preserve separate catalogs.
The independent dense-byte arithmetic test gives 8,595,571,712 bytes.

`checked_sum` and `sum_counters` check uint64 aggregates. Tests sum 3,000 records
with trillion-unit fields, reject overflow, check sourcewise conservation and
retain separate gross replacement removal/supply and external dispatch energy.

`encode_trace_event` and `decode_trace_event` require both 276-byte persistent
attachments for BOUNDARY/FAULT_BOUNDARY, making those complete events 744 bytes.
`commit_trace` streams supplied bytes in order using ASCII E3TRACE9, phase u32,
and G digest before the event stream. It hashes the supplied bytes, not cloned
objects or regenerated serialization. The helper checks indices/scalar counts,
but cannot establish that a caller supplied an entire original execution.

Canonical JSON is explicitly a restricted compatible domain: plain dictionaries
and lists, ASCII keys and strings, null, booleans, and integers with absolute
value below 2^53. All floats and custom containers reject. Decimal uint64 string
helpers and a closed count-key serializer are provided. No general RFC 8785 or
complete manifest-schema implementation is claimed.

Validation evidence:

* `python -B -m unittest -v test_e3_archive`: 49 passed, zero failed, zero skipped
* Independent literal 64-byte reset golden plus fieldwise golden layouts for
  every implemented wire family; round-trip tests are additional evidence
* Every truncation and trailing bytes rejected; individual reserved bits and
  padding bytes mutated and rejected
* Source payload row zero distinguished from absence; missing/mismatched payloads
  and out-of-range links rejected
* All 404 assigned G IDs checked against an independent forward grid
* Both edited Python files have no editor errors; Python syntax checks passed
* Final `python -B verify_e3_design.py`: all 23 frozen files passed unchanged
* No target draws, run directories, archive shards, or test-output files created

## Explicit limits and follow-on work

* [ ] Implement writer lifecycle, exclusive destinations, immutable manifests,
  shard splitting, extension bindings, and logical completeness checks
* [ ] Implement provenance, ROM/header, operand descriptors, placement/domain
  maps, dead-RLE descriptors/expansion and compact exact-alias payload storage
* [ ] Implement the closed nested manifest/gate/statistic schemas; exact recall,
  rational objectives, confidence intervals and bootstrap remain outside scope
* [ ] Validate all event-kind nonapplicable fields, legal boundary-rule pairs,
  paid paths, phase/service calendars and full roster relationships in context
* [ ] Validate lifecycle/absence reasons against original paid execution, not
  merely row bytes; technical status must not become biological death
* [ ] Establish actual-source audit/cancellation evidence, alias equivalence,
  immutable source availability and replay in fresh ownership contexts
* [ ] Compare original execution and independent whole-phase replay with G and
  complete private indexed context; suffix replay alone cannot certify a digest

Directory codec values 1/2 are recognized, but their structural round trip does
not certify lossless RLE/alias expansion. Snapshot support is the full dense
form only. Neither a table hash nor a reset checks byte certifies a complete run.

## Specification gaps and stop boundary

No contradictory byte width or arithmetic ceiling was found in the implemented
scope. No prospective version change was made or is required for these codecs.
Two details remain explicitly uncertified rather than guessed:

* Interface v0.9 names TEMPLATE visited-mask/written-mask u32 fields without an
  explicit bit-to-cell coordinate definition. Width validation is implemented;
  a global/local coordinate map is not invented.
* Interface v0.9 requires invalid BOUNDARY kind/substep pairs to reject and gives
  kind/substep ranges and rule references, but not a complete legal-pair table.
  The codec checks ranges, not the rule interpreter or pair legality.

Full semantic conformance and COMPLETE status must stop until those details are
resolved from authoritative rule context or a prospectively reviewed amendment.
They do not prevent representing the exact fixed bytes. No experimental or
original-archive integrity claim is made by the 49 component tests.

## Clarifying questions

No user input is needed for the delivered component scope. Before complete
archive certification, the schema owner must resolve mask-coordinate semantics
and the exhaustive legal boundary pairs if existing rule context is insufficient.