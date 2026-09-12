---
title: ADMIT CF-001 whole-service quote fix
description: Narrow pre-execution overflow correction with focused regression evidence.
ms.date: 2026-09-10
---

## Scope and correction

CF-001 is fixed in `run_admit`. Source and test edits are limited to the
admission module and its focused test module. The frozen review, other
modules, contracts and manifests remain unchanged. This new change record
does not revise the review or authorize runtime integration or scientific runs.

`_FULL` is computed from `meter.FEE` plus `_BODY`, yielding
`Cost(449, (1, 1, 1, 1))`. This includes the one-energy scalar delivery and
four complete 14-energy writes. The full quote dominates the 136-energy
rejection path and every suffix for all five public slots.

`meter.floor_quote(_FULL, public_tail=public_tail)` now checks full cost plus
tail plus one-energy residue before any gate, debit, payload validation or
execution. All four material sums are checked in signed-32 arithmetic too.
Overflow raises direct `OverflowError` without changing any State or Scratch
byte, including E; it is not wrapped as `AdmissionFailure` or reported as
physical shutdown. Representable but unaffordable bounds still follow the
original physical shutdown path. No threshold, tariff, reset or cleanup changed.

After paid cue delivery, assigning `None` releases the consumed cue without
the loop's previous possibly-unbound-variable diagnostics. Following payload
work still uses Scratch. Tests use fixed-size material tuples, explicit event
type narrowing and local `Any` annotations for deliberately malformed inputs;
the public API signature and paid instruction sequence are unchanged.

## Regression evidence

The exact review reproduction failed before the patch: at E=450 with
`T.energy=INT32_MAX-322` and a missing cue, the full quote was 2147483775,
but the call returned `SHUTDOWN` and changed E to zero instead of raising.
That intentional failing unittest was reported as a failure, not a passing
process exit.

One added test method checks 1,430 boundary fixtures across five slots and
E=0/450. Invalid cases include all 128 previously missed energy values,
`INT32_MAX-445`, the exact reproduction, the next post-body boundary,
`INT32_MAX`, and individual/all-source material overflow. Valid cases include
`INT32_MAX-450`, its lower neighbor and sourcewise `INT32_MAX-1` tails.
Sentinels reject any premature gate, debit, scalar delivery, core step or S.
Byte snapshots distinguish technical nonmutation from valid energy-only shutdown.

## Completed validation

Python 3.13 was the editor-selected interpreter. Each requested unittest
invocation used `-B` and returned exit code 0:

* Admission: 10 tests passed in 0.816 seconds
* Services and upkeep: 41 tests passed in 6.152 seconds
* Meter: 29 tests passed in 0.012 seconds
* Total: 80 test methods passed, with no failures

Pylance and editor diagnostics are empty for both edited Python files.
Read-only design verification passed before and after testing: 23 of 23
entries, no failures, exit code 0. SHA-256 comparison found no changes among
36 monitored protected files: other E3 modules/tests, the design manifest
and the frozen review.

The full teaching suite was not run. No broad test discovery, production
service sequence, acquisition, target draw or scientific phase was executed.
The existing final launch and confirmatory H2 NO-GO decision remains unchanged.