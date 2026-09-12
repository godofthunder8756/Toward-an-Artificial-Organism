---
title: E3 research continuation handoff
description: September 2026 audit findings, protocol status, and next pre-implementation gate
ms.date: 2026-09-09
---

## Current decision

Continue with a finite-information maintenance benchmark before adding a new
neural developmental architecture. The conventional explanation, paid error
correction plus ordinary allocation, should be implemented as the reference,
not treated as a weak afterthought. No E3 experiment was run this session.

Start with [E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md) and
[E3_LITERATURE_REVIEW_v0_1.md](E3_LITERATURE_REVIEW_v0_1.md).
They supplement, not replace, [NEW_AGENT_GUIDE.md](NEW_AGENT_GUIDE.md),
[RESEARCH_NOTEBOOK.md](RESEARCH_NOTEBOOK.md) and [E3_DESIGN.md](E3_DESIGN.md).

The protocol is explicitly unfrozen. It answers the ten conceptual questions
but lists the exact state-layout, cost, allocation and scheduling details that
must be specified before code. Do not call it an executable preregistration.
E3a's reference memory/controller is a narrower gate, not the single developing
recurrent substrate requested for the later E3b architecture.

## Fresh audit of previous evidence

The two supplied handoff copies are byte-identical. The existing 24 E1/E2 tests
pass on Python 3.13.3 with NumPy 2.2.6. The stored runs used Python 3.12.14 and
NumPy 2.3.5. No existing source, raw outcome, checkpoint, freeze or validation
report was edited. New research artifacts are separate.

The [full audit](.copilot-tracking/research/subagents/2026-09-09/existing-evidence-audit.md)
verified complete Cartesian evaluation coverage: 7,104 E0 rows, 4,480 E1 rows
and 9,216 E2 rows. Recomputed saved seed-level point estimates agree exactly.
The audit did not recompute bootstrap intervals or rerun training.

### Integrity findings that must travel with the package

* All seven E2 frozen entries match. Ten of eleven E1 entries match; the
  exception is [ENGINEERING_LOG.md](ENGINEERING_LOG.md), which now includes E2.
  A subsequent read-only check verified that its original 1,933-byte prefix
  exactly matches the frozen E1 hash. The complete current file still fails
  that hash. Do not edit the old freeze or pretend the original verifier passes.
* E1 model/configuration/protocol/test/analysis hashes are unchanged. The log
  mismatch is not evidence that its numerical model changed.
* Selected E1 replays were exact in 0/28 cases and E2 in 12/42 cases on the
  current stack. All selected discrete events and lengths agree. Maximum
  continuous differences were approximately 1.11e-16 and 7.11e-15 respectively.
  These are bounded descriptive differences, not a passed exact-replay gate.
* E0's source hash, five mechanism checks and selected 600-row replay pass.
* [PACKAGE_MANIFEST.json](PACKAGE_MANIFEST.json) is a historical v0.2 manifest,
  not a complete current package manifest. Three listed documents have changed
  since it was made; it predates the E2 additions.
* The audit's strict file-metadata preservation assertion failed because one
  pre-existing type-checker cache timestamp changed during execution. All
  5,260 inventoried original file contents were unchanged. The writer was not
  proven; no clean overall audit pass or timestamp repair is claimed.

Saved validation reports remain historical records. Current reproducibility
requires the qualifications above. A compatible numerical environment could
investigate exact replay, but even matching Python/NumPy alone would not prove
identical BLAS, hardware or floating-point execution.

A second execution of the read-only audit completed with exit code zero and
unchanged contents, sizes and timestamps for all 5,265 files in its current
inventory. It reproduced the same E1 hash mismatch and E1/E2 replay differences.
Only audit-helper type annotations and a local variable name were corrected;
its strict preservation assertion and original verifier criteria were retained.
The second run does not erase the first run's cache-metadata finding.

## New scientific constraints

No-example recovery must also be no-answer-feedback recovery. In a binary task,
action plus correctness reward reveals the answer. Energy returns, resource
access and task-dependent stopping rules can be teaching channels too.

An immediate majority vote can already tolerate missing replicas. Reconstruction
may therefore be visible only as paid restored redundancy and improved recall
after another damage challenge. A no-write control separates that benefit from
passive decoding.

Complete-loss testing must erase all acquired state, including policy, parity,
queues, caches, body distributions and random-state dependencies. Require exact
counterfactual noninterference plus a prespecified chance-precision check, not
only a nonsignificant comparison to 50%.

Scientific review corrected three proposal ambiguities: H2 now uses a fixed
retained-cue set and 128 planned useful queries rather than an impossible
all-cue denominator; its claim is limited to corrective-write/material spending
with a separate periodic-policy comparator; and four-bit erasure enumeration
is explicitly a reduced-model check requiring a production-state argument.

The code review confirms E2's protected acquired state includes learned input,
recurrent and readout arrays, a target network, replay and Adam moments. Biomass
maintenance does not reconstruct those values. E2's numerical results remain
useful evidence of partial coupling, not acquired-information self-repair.

## End-of-session record

| Field                                 | Record                                                                 |
|---------------------------------------|------------------------------------------------------------------------|
| Question tested                       | Prior evidence integrity was audited; E3 hypotheses were specified.     |
| Mechanism implemented                 | None for E3; a baseline-first finite-memory assay is proposed.           |
| Externally supplied objectives/rules   | Teaching, generic ECC, scalar ecology reward and simulator laws.        |
| Engineering changes made              | No existing experiment source or settings changed.                     |
| Frozen sample and gates               | No E3 freeze; proposed 32 final individuals and gates remain unfrozen.   |
| Primary results                       | No E3 results; prior point estimates/coverage reproduced in the audit.   |
| Simplest sufficient rival explanation | Conventional ECC, paid scrubbing and ordinary RL allocation.            |
| Failures and negative results         | E1 log-hash drift, exact replay differences, cache-metadata assertion.   |
| What this establishes                 | A qualified evidence audit and a falsifiable next protocol proposal.    |
| What this does not establish          | E3 success, a new algorithm, autonomy, life, wanting or consciousness.   |
| Files created or changed              | Three versioned E3 documents and separate tracking/audit artifacts.      |
| Verification completed                | 24 tests; source/data audit; selected replay; finite-code algebra.       |
| Next falsifiable question             | Does paid correction improve later retention without answer access?    |

## Next bounded work

1. Complete and freeze the pre-implementation specification in the protocol's
   checklist: every state bit, opcode cost, hazard, learner update, support rule
   and branch schedule. Review information isolation before simulation code.
2. After that freeze, implement the smallest conventional reference and
   exhaustive four-bit erasure/code tests, then engineering-only individuals.
   No final sample until the second source/configuration/analysis freeze.
3. Separately, improve archival packaging with a new versioned manifest and
   numerical-environment replay report. Preserve all historical hashes and
  reports; never silently regenerate them to remove these audit findings.
