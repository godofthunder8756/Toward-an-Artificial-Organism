---
title: E3 interface and archive design closure research
description: Bounded AC-01 and AC-04 decisions and information-boundary evidence for interface v0.9
ms.date: 2026-09-10
status: Complete - AC-01 and AC-04 design selected, runtime validation unperformed
---

## Questions and scope

* Select an exact ordinary and privileged worker codec without hidden acquired storage.
* Adopt completed ordinary service/ROM witnesses and information-boundary qualifications.
* Specify finite raw archive, path validation, context, replay, and statistics layouts.
* Close AC-01 and AC-04 at design level only; keep oracle linking AC-02 and scripted H2 AC-03 separately owned.
* Write only E3_INTERFACE_CONTRACT_v0_9.md and this research note; run no E3 source or random generation.

## Evidence read

* .copilot-tracking/reviews/2026-09-10/e3-b07-information-review.md, complete
* .copilot-tracking/reviews/2026-09-10/e3-b05-review.md, complete including appended v0.8 acceptance and AC checklist
* E3_EVALUATION_CONTRACT_v0_8.md, complete

## Initial findings

* B05 closes EV-001/EV-002 prospectively; AC-01 through AC-04 remain bounded design tasks, not demands for positive experimental outcomes.
* V0.8 selects eight-byte responses, 48-byte ticks, 308-byte snapshots, 64-byte reset audits, 512-byte phase summaries, and a 67,108,864-byte context allowance: 8,567,308,288 bytes total.
* The v0.8 tick capsule cannot stand alone as an audited scientific outcome or exact execution trace. Deterministic replay requires original execution commitments, exact state anchors, all input provenance, and explicitly defined raw outcomes and counters.
* B07's proposed ordinary tags need separate privileged template tags; target/run/archive identifiers never enter worker frames.

## Additional evidence

* E3_OPERATION_CONTRACT_v0_3.md, complete: eight scalar occurrences, fee-before-delivery, current-packet ownership, physical death and scratch lifetimes
* E3_CONTROL_CONTRACT_v0_6.md, complete: exact operand ABI, two prepaid controller budgets, repaired W, POL-001 through POL-003
* .copilot-tracking/reviews/2026-09-10/e3-control-review.md, CT-001 through CT-010
* .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md, incorporated instruction, A-K, liveness and variant sections
* .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md, complete
* .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md, complete
* E3_EVALUATION_CONTRACT_v0_7.md, incorporated RNG, lifecycle, diagnostics, estimands and exact bootstrap tuple sections
* .copilot-tracking/reviews/2026-09-10/e3-b06-review.md, AN-001/AN-002 and conditional erasure-assurance evidence
* E3_PHYSICAL_CONTRACT_v0_4.md, placement/domain/age definitions; E3_POLICY_CONTRACT_v0_5.md, signed objective and feedback ownership

## Selected design decisions

E3_INTERFACE_CONTRACT_v0_9.md is the sole root output. It selects:

* Binary BIND/BEGIN/SCALAR/EXIT/SHUTDOWN frames, immutable public G IDs, 284-byte BEGIN payload, six-byte scalar payloads, 276-byte sole persistent state and 32-byte scratch.
* Tags 0-20 for ordinary services and distinct tags 21/22 for four-bit privileged template cue/payload. No hidden extra dictionary, queue, saved closure, current-cue pretest, arbitrary root lookup or whole-parent read capability.
* Target/evaluator, scheduler/HMAC, physics/METER, supervisor and archive separation. Only approved current scalars cross the boundary; artifact hashes and truth IDs are archive-only. Separate-process implementation is required but is not a demonstrated host compartment or adversarial sandbox.
* Normative adoption of both completed ordinary service/ROM witnesses and CT repairs, excluding historical oracle-zero statements. The ordinary 37,536 co-resident capacity does not include v0.8 oracle sites; AC-02 remains separately owned.
* All-history actual-source canonical/reset audits, fixed G/Z comparisons, one-way probes/audit hooks and fresh-context cancellation. Active-frame audits do not create resumable checkpoints or a worker-visible queue.
* Eight-byte due responses with original/actual cue, raw slot, truth/routing, feedback-presence and survival fields. No proposed twelve-byte response is substituted for the actual v0.8 eight-byte selection.
* Forty-eight-byte tick rows: full SHA256 plus a 16-byte capsule with V/A/W, statuses, masks, selected action, raw return and target-correct/incorrect code-write counts. Per-tick C counts are reconstructed from original committed traces and preserved in phase totals, not silently narrowed.
* Fixed 308-byte snapshots, 64-byte reset audits/templates, eight-byte lessons, four-byte COMMITs and one fixed 512-byte phase schema with 62 uint64 counters. Cumulative debit/cost values use uint64, not stock or signed-return widths.
* Original streaming primitive trace commitments with exact 192-byte observer records, full before/after state extensions for physical boundaries, per-phase counts/digests and every tick's SHA256. No massive opcode archive is required; nearest-anchor replay checks local outputs, and phase-wide replay checks the original primitive digest.
* Raw reconstruction/miscorrection signs and routing outcomes are independently cross-checked against target encoding/original cues. V/A/W or final-state equality alone is not treated as proof of a unique internal path.
* Finite shared schedule, phase, class, G, ROM/operand, provenance and manifest layouts totaling 67,108,864 bytes. Sixty-four schedule slots per cell cover 34 used namespace/phase forms; no arbitrary per-history JSON.
* Complete dead suffix expansion with mandatory counts and optional lossless RLE; no technical exception becomes biological death, omitted failure rows or a COMPLETE run.
* Immutable STARTED plus separate terminal manifests, canonical JSON without nonfinite values, new replay/resume destinations, and no run/root/freeze/source files created during design closure.
* Exact equal-panel/equal-individual statistics and the inherited 10,000-replicate paired HMAC bootstrap tuple, with no bootstrap generated here. Undefined denominators and missing rows remain explicit.

## Scientific interpretation

POL-001 retains the missing-response zero versus useful-error -64 incentive limitation without adding a penalty packet. POL-002 retains short gamma=15/16 weighting. POL-003 fixes engineering-selected G before independent final targets and holds it fixed in reset comparisons.
AN-001 limits guaranteed final support to mandatory TERMINAL clearing, not optional TD. AN-002's illustrative PERIODIC probabilities are 0.619/0.204. Neither g=36 nor design closure guarantees selective spending, positive O denominators, adaptive superiority or experimental success. The canonical-empty assurance is conditional, not an observed pass.

## Verification and bounded lessons

Read-only PowerShell checked field widths, archive/context arithmetic, links, line length and evidence hashes; no E3 source, random generation, simulation, bootstrap, training or experimental replay ran.
The root contract has 290 lines before final newline normalization, below 400. All specified record sizes and three 32-bit capsule groups add exactly. Shared context is 67,108,864 bytes and dense core remains 8,567,308,288 bytes. All six adopted evidence hashes still match the reviewed files. Editor diagnostics had no errors before final readback.
One discarded draft bound incorrectly multiplied the signed-32 quote maximum by every ROM site and called it a uint64 bound. Static arithmetic exposed the error. The final bound instead uses actual debit <=65535 and remains below uint64 even under an intentionally excessive site count; quotes are not realized debits. No incorrect arithmetic output is used as evidence.
A PowerShell parser rejected member access directly on an ordered-hash expression; assigning the ordered dictionary first succeeded. Keep this lesson here to honor the only-two-files constraint rather than create unrelated memory/script files.

## Recommended next work not performed

* [ ] Complete separately owned AC-02 oracle static linking/traps/quotes and AC-03 scripted H2 product before unconditional first-freeze acceptance.
* [ ] At the authorized implementation stage, validate codec/ROM/scratch/current-packet reachability and sourcewise prefix/stock conservation.
* [ ] Execute actual-source exhaustive component and production-bit reset comparisons, clone isolation, raw-outcome checks and dense/RLE/sparse exact replay/interruption tests.
* [ ] Run authorized engineering oracle, selected controls and scripted feasibility checks only after implementation validation.
* [ ] Freeze selected G/source/tests/statistics/archive definitions before any independent final target/root draw.

No AC-01/AC-04 design blocker remains under the selected v0.9 definitions. These unchecked items are separate design ownership or later runtime evidence, not an empirical pass claim.

## Clarifying questions

None requires user input for this bounded closure.
