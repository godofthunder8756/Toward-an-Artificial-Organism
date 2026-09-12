---
title: E3 codec admission and scalar attempt fixes
description: CCI-001 and CCI-002 fixes, rank regression repair, and synthetic validation evidence.
ms.date: 2026-09-10
---

## Scope and disposition

CCI-001 and CCI-002 are resolved for the local codec boundaries reviewed in
[.copilot-tracking/reviews/2026-09-10/e3-codec-input-review.md](.copilot-tracking/reviews/2026-09-10/e3-codec-input-review.md).
The entire original review was read and remains byte-identical. Its historical
findings and recommendations were not rewritten.

Only [e3/archive.py](e3/archive.py),
[test_e3_archive.py](test_e3_archive.py),
[test_e3_protocol.py](test_e3_protocol.py), and this evidence note were edited
or created. No protocol implementation, machine, other-agent code, frozen
contract, manifest, semantic count, or experimental artifact was changed.

## CCI-001 admission consistency

[Tick capsule validation](e3/archive.py#L475-L483) rejects rather than clears:

* Nonzero `health`, `e_bin`, or `p_bin` without admitted DECIDE
* Nonzero `accepted_yield` without admitted action
* Admitted action when `action == 3` denotes absence

The [independent malformed capsule tests](test_e3_archive.py#L151) retain the
exact 16-byte review witness `80 00800100 0000000c 00000000 0000 00`.
Five additional literal rows cover E-bin, P-bin, unadmitted forage/collect
income, and admission of an absent action. All six reject as capsules and as
the capsule inside a 48-byte tick record. These bytes do not come from the
production encoder and were not normalized into valid goldens.

[Constructor and marshal tests](test_e3_archive.py#L391) cover each presence
relation, including forged frozen objects, nested tick validation, and the
explicit objective helper. Existing positive-yield and scrub fixtures now
state their DECIDE/action admission facts rather than weakening validation.

Positive fixtures retain all 16 combinations of admitted health/E/P bins,
admitted zero and nonzero resource yields, main and DRIVE returns, rejected
zero-yield selected forage, and selected zero-return forage distinct from
absent action. Acquisition REP LESSON and BLOCK COMMIT retain complete and
paid-prefix V/A/W with no controller or action admission. No V/A/W admission
gate or implicit main-objective return rule was introduced.

## CCI-002 contextual scalar attempt bound

[Scalar validation](e3/archive.py#L1074-L1077) restricts `aux` to built-in
integers 0..1023 only inside `SCALAR_IN` and `SCALAR_OUT`. The general uint32
check and existing non-scalar interpretations remain unchanged. No contextual
zero-only rule for deterministic tags or outputs was added.

The [endpoint fixtures](test_e3_archive.py#L714) and
[malformed fixtures](test_e3_archive.py#L735) cover both kinds and B/T tags.
An independently assembled 192-byte B input golden has tag 8, width 1,
`raw_after=1`, and `aux=1023`. Tests replace exactly bytes 116..119 with
little-endian 0, 1023, 1024, or 4294967295, leaving reserved padding intact.

* 0 and 1023 pass constructor, marshal, unmarshal, trace encoding/decoding,
  and exact trace commitment/count comparisons.
* 1024 and uint32 maximum reject at each boundary, including marshal of a
  forged record and commitment of independently corrupted wire bytes.
* Negative values, booleans, floats, integer subclasses, unrelated enums,
  and uint32 overflow reject.
* C/CONTROL budget, TRANSPORT action/ecological, BOUNDARY kind/substep, and
  general METER aux fixtures retain their separate encodings. A valid
  intervention/sham boundary aux of 1286 passes with both state attachments;
  METER retains 1024 and uint32 maximum.

For the actual `SCALAR_EVENT_GOLDEN` fixture, SHA256 of its 192 bytes is
`45a9a83c163c69675729053ad9f4f5b9961d1fbfa64efc63dec564763f2c4d8b`.
The one-event phase-zero commitment with fixture `DIGEST=bytes(range(32))`
is `d422591971fe028bde9157ae13958295bc21f0fe5d717301177e380153f3b893`.
It was compared against an independent SHA256 of the literal E3TRACE9 prefix,
little-endian phase, fixture G digest, and supplied bytes. Counts are exactly
one event and one scalar. These are constructed fixture hashes, not original
experiment or complete-phase provenance.

## Rank branch coverage

The [rank regression](test_e3_protocol.py#L459) now validates each BEGIN
independently before testing B/T/X rejection. All four SCRIPTED IDs 400..403
use valid ecology mask 7, so disabled learning cannot satisfy the assertion.
All 12 ID/tag combinations reject with exactly
`rank scalars require RL selection` through contextual validation, encoding,
and parsing: 36 rank-specific checks.

Ordinary PERIODIC/THRESHOLD BEGINs remain valid in development with mask 4
and reject B/T/X for the same rank-specific reason. Underlying RL ID 4 retains
positive learning-disabled rank validation and encode/parse coverage in both
development and ecology. No new FROZEN configuration selector was invented.

## Executed validation

The editor-selected interpreter is Python 3.13. All terminal Python runs used
`-B`; focused snippets set `sys.dont_write_bytecode = True` before project
imports. Initial reproduction confirmed both defects and the old rank fixture's
premature learning-guard rejection before edits. The initial archive/protocol
baseline passed 84 tests despite those defects.

Final runs:

| Run                                              | Tests | Passed | Skipped | Seconds |
|--------------------------------------------------|-------|--------|---------|---------|
| Nine new CCI tests plus repaired rank regression  | 10    | 10     | 0       | 0.028   |
| Archive and protocol suites                       | 93    | 93     | 0       | 1.647   |
| All E3 suites, unittest discovery with `-p` filter | 297   | 293    | 4       | 15.326  |

Discovery used `python -B -m unittest discover -p 'test_e3_*.py'`.
The eleven suite counts are archive 58, arithmetic 16, coding 13, design 18,
inputs 23, machine 43, meter 29, physical 25, policy 13, protocol 35, state 24.
The nine added archive tests raise the full E3 total from 288 to 297; the
protocol test count remains 35. No failures or errors occurred.

The four skips are existing Windows symlink fixtures with WinError 1314.
No elevation, privilege workaround, or native-link coverage claim was made.
The Problems/editor error query returned no errors in the three edited Python
files. A separate raw Pylance LSP query reported 155 typing diagnostics on
unchanged codec expressions: 24 `reportCallIssue`, 130
`reportAttributeAccessIssue`, and one `reportArgumentType`. None points to
the new guards. No pre-edit raw-LSP baseline was captured, so this is not a
claim of a globally clean type-checking run; out-of-scope typing was not edited.

## Integrity evidence and limits

[verify_e3_design.py](verify_e3_design.py) ran before changes and after tests,
and immediately before/after the final test runs. Every invocation returned
`ok=true`, 23 files checked, and no failures. Forty-nine distinct source, test,
verifier, review, and freeze hashes were captured before editing. Forty-six
remain identical; the only three changed entries are the authorized Python
files. The new evidence note is outside that preexisting-file snapshot.

Final changed-file SHA256 values:

* [e3/archive.py](e3/archive.py):
  `56504b358224c03e77dd0afb2407ee77ec829ab6fb4d7973ea8e815706796ef7`
* [test_e3_archive.py](test_e3_archive.py):
  `f6e2c3e1463fd6be08530cb4bda14bf272516973a4ea53432b4e0297f15ab997`
* [test_e3_protocol.py](test_e3_protocol.py):
  `e7458e393748b7ed9331bb011e776382c69da4f495b2ce26e575c185e26b2902`

Preserved SHA256 values:

* [E3_DESIGN_FREEZE_v0_11.json](E3_DESIGN_FREEZE_v0_11.json):
  `3678d797dc17485fcc823cb7f83696e4ba20c9a69921d709291cad50c3f878d4`
* [.copilot-tracking/reviews/2026-09-10/e3-codec-input-review.md](.copilot-tracking/reviews/2026-09-10/e3-codec-input-review.md):
  `17c6b06564f2980a69893e6ea542cfcd5c2511b5fb4af94b7f86afcd17676e7d`
* [e3/machine.py](e3/machine.py):
  `c46a72da4f33c000222ad788c50c24581492d1bc8bb0d1e7521bb2c414abf594`
* [test_e3_machine.py](test_e3_machine.py):
  `9c778f6951ad719e935644d15b769200cf32e85de3efe1ced7895a607deee9e4`

Only synthetic component fixtures were executed. No experiments, live target
or root draws, bootstrap matrix, full archive, or final-run promotion occurred.
Archive lifecycle, replay provenance, full boundary legality, isolation, and
other integration limits in the original review remain outside this closure.
The engineering-only design decision and semantic roster counts are unchanged.