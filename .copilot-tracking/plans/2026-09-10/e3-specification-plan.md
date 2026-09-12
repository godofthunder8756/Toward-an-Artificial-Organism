---
title: E3 specification continuation state
description: Authoritative continuation phases, artifact inventory, review findings, and ordered follow-up work
ms.date: 2026-09-10
---

## Authority and scope

All state is managed through the .copilot-tracking folder files. Scientific
deliverables supplement these records; they do not replace the execution state.
The user requested continued work after excessive compaction. Resume the first
scientific follow-up, operational specification, without implementing E3 or
modifying historical evidence. Archival replay remains a separate workstream.

The September 9 bounded research/proposal/handoff assignment is complete.
Its internal phases were A (research/audit), B (deliverables), and C
(review/discovery). The conversation's last phase before compaction was
Phase 5: Discover, contained within that internal Phase C. All closeout steps
were complete; no step, experiment, reviewer, or terminal process was running.
Future work was pending, not an interrupted implementation.

This continuation is a bounded pre-implementation slice: specify a finite-state
and delayed-query contract, check analytical constraints, review it, and retain
the remaining operational blockers. Completing the slice is not a design freeze.

## Current execution phases

1. Phase 1: Recover state. Complete: reread all ten prior tracking artifacts,
   guide, proposal, literature synthesis, design, and handoff; reconcile phase
   names and preservation limits. No historical experiment rerun.
2. Phase 2: Research constraints. Complete: independent state/timing audit;
   finite-budget, retention headroom, living-cost and precision arithmetic.
3. Phase 3: Specify. Complete: add the versioned state/temporal contract with
   exact allocation, selected query semantics and explicit remaining blockers.
4. Phase 4: Review. Complete for document consistency: a full-document reviewer
   found one Major and three Minor issues. All corrected and re-reviewed; no
   remaining finding in the bounded slice. No full operational/code approval.
5. Phase 5: Discover. Complete: record all artifacts, percentages, review
   dispositions, ordered remaining work and document/preservation checks, with
   the nonblocking final-blank-line exception below. No step remains in progress
   in this bounded slice. B02 is the next specification step, not an interrupted
   experiment or an authorized final run.

Scientific deliverable:
[E3_STATE_CONTRACT_v0_2.md](../../../E3_STATE_CONTRACT_v0_2.md).
B01 state/temporal candidate is complete as documentation. B02-B07 remain open;
operational specification has no defensible overall completion percentage.

## Tracking artifacts

Percentages describe completion of each artifact's assigned bounded scope,
not the fraction of E3 implemented. Prior artifacts remain unchanged.
Paths are relative to the workspace root; links resolve from this plan.

* 100%: [.copilot-tracking/research/2026-09-09/e3-protocol-research.md](../../research/2026-09-09/e3-protocol-research.md)
* 100%: [.copilot-tracking/plans/2026-09-09/e3-protocol-plan.instructions.md](../2026-09-09/e3-protocol-plan.instructions.md)
* 100%: [.copilot-tracking/details/2026-09-09/e3-protocol-details.md](../../details/2026-09-09/e3-protocol-details.md)
* 100%: [.copilot-tracking/plans/logs/2026-09-09/e3-protocol-log.md](../logs/2026-09-09/e3-protocol-log.md)
* 100%: [.copilot-tracking/changes/2026-09-09/e3-protocol-changes.md](../../changes/2026-09-09/e3-protocol-changes.md)
* 100%: [.copilot-tracking/reviews/2026-09-09/e3-protocol-plan-review.md](../../reviews/2026-09-09/e3-protocol-plan-review.md)
* 100%: [.copilot-tracking/research/subagents/2026-09-09/memory-maintenance-literature.md](../../research/subagents/2026-09-09/memory-maintenance-literature.md)
* 100%: [.copilot-tracking/research/subagents/2026-09-09/error-correction-literature.md](../../research/subagents/2026-09-09/error-correction-literature.md)
* 100%: [.copilot-tracking/research/subagents/2026-09-09/existing-evidence-audit.md](../../research/subagents/2026-09-09/existing-evidence-audit.md)
* 100%: [.copilot-tracking/research/subagents/2026-09-09/audit_existing_evidence.py](../../research/subagents/2026-09-09/audit_existing_evidence.py)
* 100%: [.copilot-tracking/research/subagents/2026-09-10/e3-finite-state-exact-erasure.md](../../research/subagents/2026-09-10/e3-finite-state-exact-erasure.md)
* 100%: [.copilot-tracking/plans/2026-09-10/e3-specification-plan.md](e3-specification-plan.md)
* 100%: [.copilot-tracking/reviews/2026-09-10/e3-state-contract-review.md](../../reviews/2026-09-10/e3-state-contract-review.md)

The research subagent wrote its isolated note despite a read-only request.
Record that scope deviation rather than claiming the continuation was write-free.
No historical file change was reported. Do not count that note as a full
production-state proof or an implemented model.

## Phase 4 Review inherited findings

The previous independent reviewer initially lacked workspace access. An exact
excerpt retry found three Major issues; revised excerpts closed all three.
Closure was only at the bounded, unfrozen proposal level, with zero remaining
Critical, Major, or Minor issues in the supplied scope, not full-file approval.

1. IV-001, closed: the all-cue H2 denominator made the useful-recall threshold
   impossible and branch populations incomparable. Fix U/O before branching;
   use the same 128 planned U responses, including dead/missing failures;
   retain whole-horizon viability and paired useful-recall-loss constraints.
2. IV-002, closed: fewer writes did not imply lower total expenditure. Restrict
   the claim to corrective writes/material; separately compare periodic policy;
   use ratios of aggregate individual means, retain zero-reference individuals,
   and treat a zero aggregate denominator as undefined/nonpassing. Report shared
   costs and total energy separately; retire whole blocks for the primary H2.
3. IV-003, closed: four-bit enumeration did not prove production erasure.
   Classify it as component evidence; require the complete acquired-state
   inventory, compositional noninterference, production-schema and cross-block
   tests. All 16 binary labels have 65,536 possible assignments. Chance accuracy
   cannot replace the state-boundary argument.

## Phase 4 Review latest executive findings

The named Implementation Validator again lacked file tools: no files read,
no assessment, no log. A Researcher Subagent then read the complete new contract,
prior protocol and continuation plan and wrote the independent review. A second
independent full-document pass checked the revised contract and appended closure.
This is stronger document coverage than the September 9 excerpt-only pass,
but it is not an implementation validation, operational freeze or erasure proof.

1. SC-001, Major, resolved: allocation had no current offer on required drain
   ticks or recovery-only ticks. Select a separate maintenance offer every live
   development/H2/recovery tick, matched to admissions when present and otherwise
   independently scheduled. H2's last five spending ticks still allow allocation.
   H1's entire 261-tick evaluation is explicitly response/upkeep-only. No due-cue
   lookup, remembered last offer or seventeenth cue is introduced.
2. SC-002, Minor, resolved: prior random block-code ties competed with the new
   no-write-guess constraint. Live repetition and block decoding now abstain
   on empty/tied observations. Only a unique decode can guide writes, and may
   miscorrect. Explicitly supersede the old live random-tie interpretation;
   forced-choice probe guesses remain non-writing. Opcode costs remain B02.
3. SC-003, Minor, resolved: a stored validity bit is not authenticated lesson
   receipt. Corruption may falsely accept/reject a lesson or encode a wrong
   payload. No hidden success bitmap or evaluator integrity check is available.
   Clear all eight staging bits at the scheduled opportunity; inability to
   afford retirement must follow B02, not a free clear or hidden retry.
4. SC-004, Minor, resolved: misrouting is not automatically a wrong binary bit.
   Compare emitted bits with the originally scheduled cue; coincidental correct
   bits count for binary recall and routing errors are separate. Missing/invalid
   outputs score zero. Use scheduled-cue usefulness for ecological yield; forged
   outputs without a planned response receive no yield or extra scored row.

Re-review: no new Critical, Major or Minor inconsistency; B01 document consistency
passes only. B02-B07, implementation validation and complete noninterference
remain open. Initial findings and their historical line references are retained
in the review rather than rewritten to imply an initial pass.

## Phase 5 Discover ordered workstreams

Preserve this order. The user has authorized continuation of specification work,
not automatic implementation, final runs, or archival modification.

### 1 Complete the E3 specification

1. Reload authoritative state. Done for this continuation. All further state
   remains in .copilot-tracking; distinguish closed proposal work from an
   unfinished operational contract.
2. Resolve finite representation. Candidate documented and reviewed in B01:
   160 code bits, 2,048 auxiliary bits (1,784 used), 256 operation scratch bits;
   persistent teaching/query/TD records, canonical reset, no free continuous
   storage. Replay, target networks and optimizer copies remain excluded.
   Physical/cost implementation and actual schema tests are not complete.
   Changes require a new accounting/version.
3. Resolve operations, budgets, and damage. Pending: exact reads/writes/logic,
   transport/rent/living/material costs and common budget enforcement; locality,
   write atomicity, ties/abstention/miscorrection; flips versus erasures versus
   spatial loss; code-only versus whole-substrate strata. Probe guesses never
   write back. Account for all background and query-period wear.
4. Resolve allocator and schedules. Partly addressed: a 32 x 3 signed-16 Q
   table, 1/256 units, alpha 1/8, gamma 15/16, round-to-even/saturation and
   epsilon 1/16 are candidate selections. One-step return timing avoids a hidden
   delayed-credit queue. Still require reward units, costed observations,
   updates/refresh ordering, tuning budgets, resource schedules, full branches,
   seeds/configuration and uncertainty justification. H1: 256 responses over
   261 ticks. H2: final responses 257-512 from admissions 252-507; same U/O sets
   and 128 U queries. Preserve costs during warm-up/drain and missing rows.
5. Complete noninterference design. Candidate inventory and induction documented;
   full interface/ownership review remains B07. Use 276-byte boundary snapshots,
   one-way evaluator, independently indexed future inputs, canonical queues,
   physical histories and controller values. Actual schema tests, cross-block
   checks and implemented noninterference remain pending. Chance is supplementary.
6. Close design-relevant literature and coding gaps. Pending: cost the decoder;
   existing distance algebra alone is insufficient. Obtain adaptive/flexible ECC
   full texts only before adopting their algorithms; seek persistent-corruption
   studies including auxiliary memories; obtain missing biological texts or
   compare Benna-Fusi versions before importing their detailed equations.
7. Review and freeze before implementation. Pending: full operational review,
   justified gates and precision, design-only hash manifest. A local freeze is
   not external preregistration. Only afterward consider the smallest reference,
   component/production tests and engineering-only individuals; a second source,
   configuration, test and analysis freeze precedes untouched final individuals.
   E3b remains deferred and no E3 success claim is supported.

### Immediate next specification slice within workstream 1

Continue in this order; none is authorized implicitly as simulator execution:

1. B02: costed event/lifetime schedule for single TD record, consume/emit/clear/
   insert query operations, observations, failures, stage retirement, bookkeeping
   and terminal handling; streaming decoder opcodes and all write/read charges.
2. B03: twenty upkeep-domain placements, type-specific physical hazards, rent,
   resource yields/caps/support, conservation and wear during evaluation.
3. B04: reward mapping, thresholds, refresh, fixed-policy tuning, stream mapping,
   quantization and numerical edge-case verification.
4. B05: exact paired offers/queries/noise, branch and channel products, checkpoint
   and output formats, exception policy and complete expected row counts.
5. B06: H1 versus no-write and adaptive-versus-periodic headroom separately;
   H2 viability/scarcity/positive comparator denominators; prospective erasure
   CI containment assurance under the selected output dependence, not row counts.
6. B07: noninterference/interface and full operational review; close only adopted
   mechanism literature gaps; then design-only manifest before simulation code.
7. After design freeze and authorization: smallest conventional implementation,
   component and production-schema tests, engineering-only individuals, then
   second source/configuration/test/analysis freeze before final individuals.

### 2 Strengthen archival reproducibility

1. Provision a separate Python 3.12.14 / NumPy 2.3.5 environment; record numerical
   library and hardware provenance. Pending, not started.
2. Investigate exact replay without modifying traces or acceptance criteria.
   Pending; small diagnostic differences remain distinct from exact acceptance.
3. Use an isolated read-only copy and control background writers when strict
   metadata preservation is required. Pending.
4. Preserve both prior outcomes: first audit unchanged contents but cache-mtime
   failure; second audit 5,265 files unchanged in bytes, sizes and mtimes.
5. Only if separately authorized, create a new versioned manifest or erratum
   documenting appended E1-log drift and the historical v0.2 manifest scope.
6. Never overwrite historical manifests, freezes, validation outputs, raw final
   results or engineering history. No E1/E2 training rerun is needed for this work.

## Preservation and interpretation

Historical tests passed 24/24 in the prior session; they have not been rerun here.
E1 remains 10/11 frozen files matching; E2 7/7. Selected exact replays were 0/28
and 12/42 respectively. The successful audit wrapper did not make the original
verifiers pass. Preserve these qualifications and source-access limitations.

Ordinary error correction plus ordinary allocation remains the mandatory rival
and may explain every future E3a success. Restoring protected information access
is not regeneration of deleted information. Functional motivation, organismal
autonomy, and subjectivity remain distinct. E3 implementation is 0%.

## Continuation validation and changes

New scientific contract plus three new tracking artifacts: this plan, independent
research note and full-document review. No historical source, protocol, prior
tracking record or result is intentionally edited. The subagent research note's
unaligned tables were converted to lists without changing its candidate choices.
Its alternate five-record layout is research, not the selected one-record schema.

PowerShell scalar checks, without E3 execution, verified 2,048 auxiliary bits,
2,464 total allocated bits, all query-window counts, 32 minimum replacement writes,
128 minimum write-energy units and 6,224 recovery/evaluation living units.
At p=0.1, clean three/five accuracy is 0.972/0.99144 (gain 0.01944).
After h=0.001 for 128 ticks, unrepaired odd-flip probability is
0.11302822537825702; challenge effective probability 0.19042258030260562;
three-copy accuracy 0.9050274573516492. Optimistic perfect-repair headroom
0.08641254264835074 is not an empirical or affordable-policy prediction.

Normal-approximation half-widths 0.043310290347676035 (fixed repeated answers)
and 0.003828125 (fresh independent guesses) are sensitivity checks, not sample
approval or calibrated bootstrap results. No final targets/results were read.

Initial documentation check found missing final newlines and unaligned tables
in the research note. Corrected with file patches, not shell rewrites. The
repeat lesson from September 9 is to inspect EOF after creating files; editor
diagnostics alone do not catch the complete documentation contract.

Pre-closeout format/link check: four new documents, zero issues. Verified frontmatter,
no duplicate H1, table alignment, whitespace, final newline and local links.
Preservation comparison: 5,277 baseline files, zero unexpected content/size or
mtime changes, zero removals. Two intentionally revised new tracking files were
allowlisted (this plan and the research note). The only additions since that
snapshot were the scientific contract and independent review. The initial
snapshot was taken after the new plan/research note existed; this is not a
claim to have snapshotted the entire conversation before any tool call.

The final scientific contract hash is
0040C21E3B3A46E02000F0F9A201264A621A641686CA3658A6ED7FED3AE2E1BD.
The independent re-review hash predates a final-newline-only correction. That
change adds no scientific content and does not constitute a design freeze.
Earlier review hashes remain historical, not silently rewritten.

After the last handoff append, this plan again retained an extra EOF blank line.
Three automated correction attempts did not persist. The user was asked and
delegated autonomous judgment while unavailable. Accept this one cosmetic
exception rather than keep retrying. It changes no specification, inventory,
review finding or evidence. Do not call the final strict EOF check a pass;
final validation must report the exception separately from substantive checks.

## Bounded continuation handoff

* Question tested: can the proposed finite state and delayed-query semantics
   be specified consistently without hidden persistent copies?
* Mechanism implemented: none; state, temporal and reset candidate specified.
* Externally supplied objectives/rules: fixed ECC, Q update, public cue routing,
   task-dependent ecological return, neutral isolation inputs and simulator laws.
* Engineering changes: none to experiment code, data, settings or historical files.
* Frozen sample/gates: no E3 freeze; earlier prospective gates remain unfrozen.
* Primary results: document consistency and scalar design checks, not E3 data.
* Simplest sufficient rival: conventional paid ECC plus ordinary allocation.
* Failures/negative results: named validator could not read files; replacement
   full review found four corrected issues; initial formatting check failed;
   clean-replica gain alone does not meet the proposed five-point H1 gate.
* Establishes: bounded finite-state/temporal candidate and reviewed information
   boundary requirements; exactly accounted 2,464-bit allocation.
* Does not establish: a feasible resource budget, complete operational protocol,
   production erasure, E3 success, novelty, neural autonomy or subjectivity.
* Files created/changed: the new scientific contract and three new tracking
   artifacts listed above; no prior tracking artifact changed.
* Verification: independent full-document review/re-review, arithmetic checks,
   documentation checks and snapshot comparison; no historical test/replay rerun.
* Next falsifiable question: can a fully costed event schedule sustain paid
   correction and useful recall with this finite state and no answer access?

Last phase at closeout: Phase 5: Discover. Completed steps: inventory and
percentages, review closure, ordered follow-up work, validation and handoff.
In-progress step: none. Remaining steps within this bounded slice: none.
Remaining program work: B02-B07 in the order above, then separately gated
implementation/engineering; archival workstream remains separate and unstarted.

