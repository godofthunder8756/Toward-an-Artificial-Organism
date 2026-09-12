---
title: E3 codec and indexed-input code review
description: Read-only review of archive and input primitives, protocol regression, and synthetic conformance evidence.
ms.date: 2026-09-10
---

## Status and scope

Complete for the captured component scope. Two medium/P2 archive validation
defects are reproducible: CCI-001 and CCI-002. No new input-generation defect
or protocol implementation regression was established. E3-COMP-001 is closed
in the captured protocol implementation. This is not an unconditional codec,
archive, security, isolation, or runtime-conformance pass.

Read e3/archive.py, e3/inputs.py, test_e3_archive.py, test_e3_inputs.py,
e3/protocol.py and test_e3_protocol.py in full. Reviewed the prior component
review, the archive/input implementation scope notes, physical fault ordering,
and retained contracts. Executed all ten explicitly named E3 component suites
and additional in-memory synthetic fixtures. No experiments, target draws,
live keys, bootstrap matrix, worker execution, or full archive were generated.

Only .copilot-tracking/reviews/2026-09-10/e3-codec-input-review.md was authored.
Source, tests, contracts, manifests, historical reviews, and experimental
artifacts were not edited. No source fix, dependency install, formatting pass,
or bytecode generation was requested or performed.

## Questions

* Does every public codec and input boundary reject invalid types, oversized
  integers, reserved bits, invalid presence patterns, and ambiguous references?
* Do golden bytes, restricted RFC 8785 tuples, HMAC rejection sampling, schedule
  slots, and physical fault ordering match the frozen contracts?
* Are the component findings closed, including SCRIPTED learning and ordinary
  TICK/UPKEEP behavior, without regressions in public configuration validation?
* What do synthetic fixtures, regression suites, and freeze verification prove,
  and what remains outside this pure-library review?

## Findings requiring source changes

### CCI-001 P2 Capsule accepts observations with no admitted DECIDE

Location: e3/archive.py:458-482, `TickCapsule._validate()`; propagated through
e3/archive.py:1489-1510, `marshal()` and `unmarshal()`.

E3_INTERFACE_CONTRACT_v0_9.md:126-139 requires unreached fields to be zero with
their status/consumption flag false and says controller health is meaningful
only after admitted DECIDE. Validation checks field widths, V/A/W, write totals,
yield bounds and absent offer fields, but omits the observation-presence check.

Independent sixteen-byte counterexample:

```text
80 00800100 0000000c 00000000 0000 00
```

It has funded TICK, outer ordinal 0, no selected action (`action=3`),
`decide_admitted=0`, and `health=3`. `unmarshal(TickCapsule, raw)` accepts it;
re-encoding reproduces exactly the same invalid bytes. An assertion requiring
`ArchiveError` failed. Equivalent constructor cases with `e_bin=1` or `p_bin=1`
and DECIDE unadmitted also round-trip. This requires no original trace or
unknown manifest context to reject: the contradiction is in one capsule.

Additional same-validator witness: `action=0`, `accepted_yield=64`,
`action_return=16`, `action_admitted=0` passes, including main-objective return
validation. E3_POLICY_CONTRACT_v0_5.md:63-66 requires rejected resource bodies
to receive no yield and have F=C=0. The existing return helper checks the
arithmetic, not admission consistency.

Impact: malformed observer rows can report an observation or accepted action
income that their own admission bits rule out. A strict byte round-trip alone
does not establish semantic validity. No corrupted experiment or sandbox
escape was observed.

Proposed exact fix, not applied:

* In `TickCapsule._validate()`, reject nonzero `health`, `e_bin`, or `p_bin`
  whenever `decide_admitted == 0`.
* Reject `accepted_yield != 0` whenever `action_admitted == 0`, and reject
  `action_admitted != 0` when `action == 3`.
* Reject rather than clearing fields. Preserve `action=3` as absence and a
  genuinely selected zero-return forage as `action=0`.
* Do not blindly gate V/A/W on controller/action admission: those fields also
  represent REP LESSON/BLOCK COMMIT in acquisition. Do not force a main-objective
  return on DRIVE or discard paid-prefix evidence.

Regression tests should exercise the constructor and independent malformed
wire bytes for each rejected presence relation. Keep positive cases for
admitted zero/nonzero observations, admitted zero-yield actions, ordinary and
DRIVE returns, and acquisition code writes. Three admitted-DECIDE observation
neighbors were independently checked and remain representable. Existing
positive-yield fixtures built from `capsule()` omit admission flags; update
those fixture flags rather than treating their current round-trip as authority
to preserve the contradictory presence pattern.

### CCI-002 P2 Scalar trace accepts impossible generation attempt indices

Location: e3/archive.py:1066-1081, `PrimitiveEvent._validate()` scalar branch.

E3_INTERFACE_CONTRACT_v0_9.md:97 and 203 fixes attempts at 0..1023 and defines
ordinary scalar `aux` as the accepted external generation-attempt index, zero
for deterministic input. The validator only checks `aux` as general uint32
before checking the scalar's tag, width and value; it never narrows scalar aux.

Reproduction used a synthetic `SCALAR_IN` B event with tag 8, width 1,
`raw_after=1`, and valid `aux=1023`. In its 192-byte serialization, replacing
bytes 116..119 with little-endian 1024 still passes `unmarshal(PrimitiveEvent,
raw)`. An assertion requiring `ArchiveError` failed. Values 1024 and
4294967295 also pass constructor/round-trip checks on a T scalar. The current
`inputs.uniform()` can never produce either attempt index.

Impact: the archive accepts scalar provenance outside the frozen input law.
It can commit such rows, while a conforming generator/replay cannot supply
that accepted-attempt coordinate. This is a local tag/kind-dependent range
defect, not the separate absence of an original-execution witness.

Proposed exact fix, not applied: inside the `SCALAR_IN`/`SCALAR_OUT` branch,
validate `aux` as a built-in integer in 0..1023. Leave non-scalar aux encodings
unchanged. Contextual enforcement of zero for deterministic tags/outputs is
additional future work; the universal 1023 upper bound needs no such context.

Regress both scalar kinds at 0, 1023, 1024 and uint32 maximum through constructor,
marshal, unmarshal and trace commitment. Keep separate tests for valid C,
TRANSPORT and BOUNDARY aux meanings. Do not mask a bad index or normalize it
to zero. The existing trace scalar test covers 1023 but not 1024.

## Prior finding closure and protocol regression

E3-COMP-001 from
.copilot-tracking/reviews/2026-09-10/e3-component-review.md is closed for the
current source: e3/protocol.py:470-493 requires the learning bit for script G
in ordinary ECOLOGY, excluding entry ISOLATE. It applies to contextual BEGIN
validation, contextual encode/parse, and the BEGIN supplied to SCALAR checks.

The repository regression at test_e3_protocol.py:438-457 checks all four script
IDs, first/due ticks, CONTROLLER, RESPONSE and TICK, plus permitted neighbors.
Additional checks covered ticks 1, 6, 507, 508 and 512; TICK, CONTROLLER,
RESPONSE, ADMIT where scheduled, AGE_LOW, AGE_HIGH, CONDITION and scheduled
TERMINAL. Results: 170 positive script/neighbor contexts, 396 rejected disabled
BEGIN operations across validate/encode/parse, and 60 rejected scalar contexts.

Mask interpretation is correct: bit0 learning, bit1 corrective, bit2 due.
Masks 3/7 enable learning before/after due starts; masks 2/6 disable it.
There is no service-local permission exemption for ordinary TICK or upkeep.
TERMINAL already requires learning structurally. Entry ISOLATE, nonlearning
reset recovery and assay remain valid. Ordinary RL ecology with learning off
remains valid FROZEN behavior; PERIODIC/THRESHOLD remain nonlearning.

All 404 archive G IDs matched protocol configuration code, policy, cuts,
interval, h, objective and variant. No assigned BIND ID has policy FROZEN=4:
FROZEN binds the underlying RL G, not configuration ID 4 as a new selector.
ID 400 is a valid public script constant, not a private key. Both booleans,
same-value float, oversized and negative configuration IDs reject. Script
`PublicConfiguration.family` being `None` while archive G uses H2=1 is
intentional: no new worker family selector was introduced.

One test-coverage regression remains: in
`ContextTests.test_rank_inputs_absent_for_fixed_and_script_but_present_frozen_rl`
at test_e3_protocol.py:459-469, script cases supply learning-disabled ecology.
The new BEGIN guard now rejects them before the rank-specific check. The test
still passes but no longer tests SCRIPTED rank exclusion independently. Own
checks with valid learning-enabled mask 7 rejected all 12 combinations of
four script IDs and B/T/X for the exact reason `rank scalars require RL
selection`. Correct that existing fixture in a later change to retain branch
coverage; no new protocol source defect was found.

The component review is NOT an entry in E3_DESIGN_FREEZE_v0_11.json. Its
contents were nevertheless left unchanged; this separate note records closure
without rewriting historical findings. Several other named reviews are
manifest entries and remain frozen. Design integrity does not freeze these
new Python sources/tests or authorize final execution.

## Public surface and type review

Every locally defined public function/method and record family in the two new
modules was inspected. Imported standard-library names are not treated as
component APIs. Existing tests cover all 18 archive record families.

### Archive surface

* `Stocks`, `ResponseRecord`, `TickCapsule`, `TickRecord`, `SnapshotRecord`,
  `ResetAuditRecord`, `LessonRecord`, `CommitRecord`, `TemplateRecord`,
  `SummaryCounters`, `SummaryRecord`, `DirectoryEntry`, `PrimitiveEvent`,
  `TraceCommitment`, `ScheduleRecord`, `PhaseDescriptor`, `ClassMapping` and
  `GRecord` inherit `_Record.__post_init__()` validation. `marshal()` revalidates
  the exact record type; nested stocks/counters/capsules require exact types.
  CCI-001/002 are missing cross-field ranges, not constructor bypass bugs.
* `checked_sum()`, `sum_counters()`, `SummaryCounters.from_values()`,
  `SummaryCounters.padding()` and `SummaryRecord.validate_accounting()` retain
  exact uint64 sums/products and sourcewise accounting. Negative padding and
  intermediate overflow reject, not wrap/saturate. The `values` properties are
  projections of constructed records, not ingestion or access-control APIs.
* `validate_row_range()`, `validate_directory()`,
  `validate_snapshot_links()` and `validate_phase_links()` check their stated
  capacities/extents and exact record/container types. Global row zero resolves
  as a real reference. Empty sums/ranges do not allocate the represented tables.
* `TickRecord.from_state()` and `verify_state()` hash exact immutable 276-byte
  inputs. `ResetAuditRecord.require_complete_checks()` checks asserted bits,
  not actual cancellation. `DirectoryEntry.verify_payload()` checks exact
  supplied range length/hash, not whole-file authenticity or decompression.
* `encode_trace_event()`, `decode_trace_event()` and `commit_trace()` preserve
  exact event bytes and require both boundary state attachments. Trace event
  indices are contiguous per tick/off-clock operation and ticks cannot reverse.
  Original provenance and full-phase completeness are explicitly not certified.
* `GRecord.from_id()` and `validate_id()` check assigned IDs 0..403 against
  the fixed grid, default script/DRIVE cuts, objective and variant.
  `TickCapsule.validate_action_return()` correctly takes an explicit objective;
  a correct arithmetic equality does not repair CCI-001 admission inconsistency.
* `marshal()`/`unmarshal()`, `uint64_string()`/`parse_uint64_string()`,
  `count_catalog_json()`, `canonical_json()` and `parse_canonical_json()`
  distinguish checked binary integers from JSON-safe IDs and decimal strings.
  Count-key serialization is not a COMPLETE-manifest or expected-count validator.

Additional numeric sweep: 5,565 substitutions rejected across scalar and tuple
elements of the 18 archive fixture records. Values included True, False,
same-value floats, int subclasses, an unrelated IntEnum, and both signs of
2^128. Another 78 public numeric-argument cases rejected. Eleven available
declared-enum fixture fields also accepted equivalent built-in integers.
The rule is exact built-in int OR the specifically declared enum, never any
arbitrary int subclass or another enum class with an equal value. JSON booleans
remain intentionally valid only in the restricted metadata domain.

### Indexed-input surface

* `InputTuple`, `InputRecord` and `PhaseContext` validate their constructors.
  `canonical_tuple()` rechecks the tuple, and every context-consuming generator
  checks the exact context and its post-init constraints. Properties
  `InputRecord.attempt` and `PhaseContext.rule/family/phase/horizon/schedule_id`
  derive from these validated objects.
* `canonical_tuple()`, `indexed_digest()` and `uniform()` require the exact
  tuple, immutable 32-byte key where applicable, and bounded built-in integers.
  Tuple coordinates are nonnegative through 2^53-1; attempts are 0..1023.
  Uniform bound is 1..2^128; nonzero starting attempt rejects.
* `phase_context()`, `reset_context()` and `generate_schedule()` select the
  explicit catalog; engineering/final identity limits, CORE-only-final,
  engineering diagnostics, and oracle panel-one restrictions are enforced.
* `fault_coordinates()`, `fault_inputs()`, `fault_thresholds()`,
  `challenge_inputs()`, `exploration_inputs()` and `guess_input()` validate
  their phase/tick/value domains. SCRIPTED consumes no B/T/X; planned unused
  guesses and ordinary faults do not shift future coordinates.
* `usefulness_assignment()`, `hub_assignment()` and `bootstrap_coordinate()`
  preserve their ecology/injury/analysis-only index rules. Bootstrap syntax was
  checked with public single-vector fixtures, not a bootstrap matrix or result.

All 15 public top-level input functions received malformed argument checks:
261 rejections, plus 84 numeric substitutions in validated dataclasses.
Both booleans, wrong scalar/container types, int subclasses, unrelated enums,
oversized/negative integers, and mutable/incorrect-length keys were included.

`ScheduleRule`, `Schedule` and `UsefulnessAssignment` have no `__post_init__()`.
They are catalog/output carriers, not accepted ingestion parameters of a public
generator. Their frozen annotation does not deep-freeze a manually supplied
list or validate a forged constructor value. Generated outputs and the fixed
catalog contain tuples/validated records; no current consumer trusts a supplied
carrier to authorize execution. This is an explicit API limitation, not an
observed generation bug. Future adapters must validate their own input boundary.

## Format and input-law evidence

### Golden bytes, widths and absence

Independent literal/fieldwise goldens cover all implemented record families,
including every capsule bit offset and each of the 62 uint64 summary slots.
The archive suite tests every truncation, suffix, reserved padding bit and
unused schedule tail nibble. Re-encoding rejects noncanonical wire padding;
it does not silently repair bytes. CCI-001/002 demonstrate why that comparison
alone cannot reject a value whose invalidity is omitted from `_validate()`.

Opaque raw body/scratch contents must not be normalized. All-zero, all-FF and
position-varying 276-byte bodies round-tripped and resolved exactly in added
snapshot fixtures. Corrupt reservoir high bits and reserved state bytes are
not protocol padding. Summary values above 2^53 and IEEE-NaN-shaped uint64
bit patterns remain exact integers, not floats, missing values or zero.

Reference zero is not absence. Snapshot payload/context zero serialized to
eight zero bytes and required actual row-zero resolution. `None` serializes
to all-ones, including uint32 0xFFFFFFFF and the narrower reference widths.
Passing 0xFFFFFFFF as a purported row ID rejects. Missing or differing finalized
payload offsets/bytes reject; identical contents do not license a live reference.

### Restricted RFC 8785 and HMAC

RFC 8785 sections 3.2.1-3.2.4 and Appendix B support the implemented restricted
domain: ASCII escaping/order, compact UTF-8, and integers through 2^53-1 have
the required ECMAScript serialization. Neither helper claims full JCS support
for arbitrary Unicode or floating-point values. Restricting accepted types is
valid here; installing a general serializer is not necessary to fix a defect.

Own independent escape oracle checked all 128 ASCII codepoints, including
the five short control escapes, lowercase Unicode escapes, quote/backslash,
literal slash and DEL. Parsers rejected same-value noncanonical encodings:
negative zero, whitespace, exponent/float form, duplicate equal-valued keys,
escaped ordinary characters, escaped slash and an out-of-domain integer.
Canonical decimal uint64 maximum round-trips without float conversion.

RFC 4231 known answers and a separate RFC 2104 ipad/opad construction pass.
All 3,160 draws for one constructed SCRIPTED final-tick fault frame were also
cross-checked against an independently assembled HMAC, not merely selected
slots. HMAC uses the supplied root as the key and the exact tuple as message;
the outer hash includes the key-derived opad, not a plain hash of the tuple
or a hash seeded with target outputs. No secret output is used as a key source.

For m=10000, the exact rejection threshold is
340282366920938463463374607431768210000. The top 1,456 uint128 values reject.
Own forced-digest tests checked each of those 1,456 values advances to attempt
one, and all 10,000 values immediately below the threshold yield each residue
exactly once. Exhaustion made exactly 1,024 calls with attempts 0..1023 and
raised `InputGenerationError`. Existing fixtures also accept the last possible
attempt, distinguish first-sixteen-byte little-endian from the unused tail,
and cover m=1, m=3 and m=2^128. These are exact mapping checks, not a statistical
claim that an empirical histogram proves cryptographic independence.

### Schedules, faults and reset class boundaries

All 35 schedule slots 0..34 match the ordered contract catalog and preserve
`schedule_id = 64*cell + slot`. Own generation checks covered all slots with
public fixture keys, expected lengths and no duplicate coordinates. Final CORE
namespace fixtures use no final live roots or labels and execute no experiment.

Acquisition has sixteen grouped passes, 256 lessons and 64 COMMIT opportunities;
recovery has 128 offers; development has 2043 admissions plus five drains;
ecology has 251 early plus 256 endpoint admissions and five drains. Independent
descending Fisher-Yates tests use swap ordinal, not the descending list index.
Drains use actual planned ticks and separate purposes, never the original due
cue. Whole-block and mixed U/O, balanced HUB assignments, and challenge versus
FLIP purpose separation pass.

Fault order matches `physical.FAULT_SLOTS` exactly: 80 code flip/erase pairs,
then 1000 auxiliary/reserve bit0/bit1/erase triples in lane order. Reservoirs
900..923 are excluded; reserve remains included. Total is 3,160, not 3,160
worker packets. Every age's flip/erase thresholds match physical integer
comparisons on 0..9999. Simultaneous pre-fault age handling remains physical
execution's responsibility; ordinary faults are not changed by SCRIPTED.

RESET inputs use base H1/H2 and RESET-RECOVERY/RESET-FINAL, intentionally omit
source product/history/branch/code/policy/budget/cuts, and preserve individual/
panel. Thirteen attempted parent/G/cut/branch keyword injections rejected.
G IDs 0/1 and script IDs 400/401 retain different serialized G even where their
normalized input contexts agree. Equal Z, predictions, bins or score does not
mean equal complete G or permission to alias trajectories. FROZEN normalizes
to underlying RL; script G does not normalize to ordinary RL.

`ClassMapping` currently checks widths/catalog bounds, not cross-record G,
parent, reset schedule or equivalence. Constructed mismatched class code/family/
config/schedule combinations can round-trip. `ScheduleRecord` likewise is not
the complete phase-slot/calendar validator, and `validate_phase_links()` checks
extents rather than parent identity or cycles. These are explicitly deferred
full-roster relationships in the implementation scope, not a claimed alias
validator. Require contextual negative tests for G/cut/parent/schedule switching
before any class sharing. No alias/security pass is inferred here.

### Integrated counts and pure-library boundary

The checked combined capacities are 129700128 ticks, 111718400 responses,
285616 summaries/phases, 3829888 snapshots, 225712 actual-source reset audits,
and 29952 canonical future slots; trunk remains 29696. Planned outer services
are 3320673872 and ordinary fault coordinates are logically 409839208320.

Exact dense arithmetic is core 8567308288 plus extension 28263424 equals
8595571712 bytes, including 71303168 shared context bytes. The script increment
retains 512 source audits and 256 canonical futures, not 256 independent
observations. This is approximately 8.5956 decimal GB, not a strict 8.5 GB limit,
allocated artifact, measured runtime, or implemented full runner.

`commit_trace()` hashes the supplied original-byte stream and checks local
ordering; it does not verify that it came from original execution or includes
the whole phase. Synthetic events, incomplete suffixes starting at zero, and
self-consistent but unproven hashes are not COMPLETE evidence. The module
expressly documents that limitation, so it is not reported as a bug.

## Validation

The editor-selected interpreter was Python 3.13. Existing suites ran with -B:

```text
python -B -m unittest -v test_e3_archive test_e3_inputs test_e3_protocol test_e3_state test_e3_coding test_e3_arithmetic test_e3_physical test_e3_meter test_e3_policy test_e3_design
Ran 245 tests in 9.966s
OK (skipped=4)
```

Archive/input/protocol contributed 49/23/35 tests. In total, 241 passed,
four skipped and none failed or errored. The skips were the known Windows
symlink fixtures with WinError 1314; metadata/reparse rejection fixtures passed.
No elevation, junction workaround or repeated privilege attempt was made.

Separate expected-contract reproductions ran two unittest tests in 0.003s:
two assertion failures, zero errors, both `ArchiveError not raised`, proving
CCI-001/002 independently of the passing repository suite. The surrounding
ad hoc process deliberately asserted that these two failures occurred and
returned exit zero; that process exit is NOT a passing result for those tests.

Ad hoc checks set `sys.dont_write_bytecode = True` before project imports and
used in-memory records and public keys only. Private `_digest` patches were
local test seams, not public callbacks or production key substitutes. Existing
verifier tests create/clean their own temporary fixtures outside this workspace.
Tool execution logs may be retained externally by the editor.

Both before and after tests, `python -B verify_e3_design.py` returned
`ok=true`, 23 entries checked, no failures. All 23 separately captured source,
test, verifier, manifest and prior-component-review hashes were unchanged.
Editor diagnostics reported no errors in the six principal Python files.
There is no workspace .git directory; no Git clean-tree or source-freeze claim
is made. These hashes capture content, not a filesystem lock.

Captured principal source hashes:

```text
e3/archive.py 40ba9e762bd9964a6b0a462a6a4d1278a5832e421b33a4341037423a5162a9e4
e3/inputs.py 9136cb3f0fc014da7e39796a22166f988480304af68064e1ef63c87982d21397
e3/protocol.py ef4978f4d0b7aa534d5adb135c7dea101888f051d3dc822a9def13f08fee7fed
test_e3_archive.py 3ad84724dbe22a5af196136265be48e9dce60f8d011df62256c04b21a119f16b
test_e3_inputs.py 8c3cb6f404316f9902526090f3fa6e8903dd966cdbae00162b4c3d42105e09c3
test_e3_protocol.py e4c4046c123d5f24bd86527044620e7659a5a09f92b3c2bb420d46d1e0d3ec76
E3_DESIGN_FREEZE_v0_11.json 3678d797dc17485fcc823cb7f83696e4ba20c9a69921d709291cad50c3f878d4
.copilot-tracking/reviews/2026-09-10/e3-component-review.md 98540908dd8fa1a7ee69f1c2ddf15a7ff6fadf11c5e8a10ff1296c22db20d423
```

## References and limits

Normative precedence: E3_INTEGRATION_DECISION_v0_11.md, explicit
E3_CONFORMANCE_CONTRACT_v0_10.md amendments, E3_INTERFACE_CONTRACT_v0_9.md,
E3_EVALUATION_CONTRACT_v0_8.md and its retained input law from
E3_EVALUATION_CONTRACT_v0_7.md. Controller ordering and resource feedback use
E3_CONTROL_CONTRACT_v0_6.md and E3_POLICY_CONTRACT_v0_5.md.

Scope evidence: .copilot-tracking/changes/2026-09-10/e3-archive-implementation.md,
.copilot-tracking/changes/2026-09-10/e3-input-implementation.md, and
.copilot-tracking/reviews/2026-09-10/e3-component-review.md.

External references consulted:

* [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), restricted-domain string,
  number, ordering and UTF-8 rules
* [RFC 2104](https://www.rfc-editor.org/rfc/rfc2104), keyed inner/outer HMAC
  construction
* [RFC 4231](https://www.rfc-editor.org/rfc/rfc4231), published HMAC-SHA-256
  test cases 1, 2 and 6

Key shape and known-answer vectors do not establish independent root requests,
live-key protection, paid scalar consumption or worker access denial. `inputs`
returns private coordinates/digests/generation evidence to the trusted caller;
these must never be delivered as worker objects. Only the authorized current
scalar value may cross a later paid adapter. Source conventions for subpurpose
spellings and swap/local indices are explicit but still require later source/
provenance binding; no live root loading was inspected or performed.

Remaining integration is not silently counted as additional component bugs:
writer lifecycle and manifests; complete nested schemas; ROM/provenance/map
codecs; dead-RLE/compact alias expansion; full event nonapplicable-field and
boundary-rule legality; complete roster links; actual-source reset/cancellation;
original versus independent replay; and process isolation. TEMPLATE mask
coordinates and the exhaustive boundary kind/substep matrix need authoritative
resolution before complete archive certification. No final or security gate
passes from these codec tests.

## Recommended next work and clarifications

* [ ] Fix CCI-001/002 in a separately authorized source change and persist the
  independent malformed-byte regressions. Re-run all E3 suites and freeze checks.
* [ ] Repair the SCRIPTED rank-test context so rejection cannot be satisfied
  prematurely by the new learning guard; retain upkeep and scalar-context tests.
* [ ] Before trusting aliases, test complete-G/cut/parent/schedule mismatches
  and actual populated/corrupt/dead source reset/cancellation independently.
* [ ] Resolve remaining archive/context schemas and prove full original/replay
  agreement and paid adapter ownership with bounded conformance fixtures.
* [ ] Run native Windows link/junction integration checks in an appropriate
  environment later; accepted skips do not establish native coverage.

No user clarification is required to understand or reproduce the two findings.
No source changes, experiments, final targets or automatic promotion are
authorized by this review. V0.11's engineering-only/no-final decision remains.