---
title: E3 policy implementation research and changes
description: Contract evidence and validation for engineering-only policy and design verifier components
ms.date: 2026-09-10
---

## Status

Complete. Scope is e3/policy.py,
test_e3_policy.py, verify_e3_design.py, test_e3_design.py and this optional
research/change record. No runner, final draws or empirical outputs are authorized.

## Research questions

* Confirm current arithmetic selector/return APIs and normative fixed/script rules
* Confirm immutable parameter domains, public clock and policy enumeration boundaries
* Determine read-only freeze verification requirements and isolated fixture coverage

## Evidence

* e3/arithmetic.py exposes select_action(q_values, b, t, x) and action_return(action, accepted_energy, accepted_material, completed_writes, n).
* E3_DESIGN_FREEZE_v0_11.json declares engineering_only_design_freeze with 23 file entries and no final or confirmatory permission.
* E3_POLICY_CONTRACT_v0_5.md selects observation s=16u+8e+4p+h, current damaged Q, no RL resource override, fixed resource priority, the nine cut pairs, periodic powers of two 1..256 and DRIVE's selected-scrub return16.
* E3_CONTROL_CONTRACT_v0_6.md supersedes v0.5's older single-envelope worksheet; its fixed selector uses the public planned clock and preserves DRIVE return across failed ACTION.
* E3_CONFORMANCE_CONTRACT_v0_10.md selects SCRIPT-U's u=1/h=3 trigger and SCRIPT-ALL's h=3 trigger after resource priority. Real script services owe genuine TD bookkeeping and 270 diagnostic padding energy, with no selection Q/rank input.
* E3_INTERFACE_CONTRACT_v0_9.md and e3/protocol.py retain codec RL/PERIODIC/THRESHOLD/DRIVE/FROZEN=0..4 and SCRIPT_U/ALL=5/6. NO_MAINT has no selected codec ID. FROZEN uses underlying RL selection with learning disabled.

## Findings and changes

* e3/policy.py adds string Policy, frozen/slotted PolicyConfig, decide and policy_action_return. No state, Q table, learned encoding, clocks, IDs, histories or packets are retained.
* decide validates exact built-in integers, immutable three-word signed16 tuples, observation0..31, positive uint16 planned ticks and B/T/X ranks. RL/DRIVE delegate selection to the existing arithmetic implementation. Fixed/scripts do not call it.
* Fixed/script Q/rank arguments are local placeholders when unused, not permission to read Q or consume packets. Common scans, CONTROL work, padding, action gates and learning services remain outside this component.
* Cuts follow the normative nine-pair whitelist; DRIVE/scripts permit default32768/64 only. PERIODIC defaults to8; other intervals canonicalize to0. These checks restrict constants but do not prove their provenance or generic-G invariance. The future integrator must hold G fixed and freeze engineering selections before independent final targets.
* policy_action_return delegates main completed-prefix validation and returns to arithmetic.action_return. DRIVE substitutes16 for scrub and0 otherwise, including failed ACTION with selected scrub. None denotes no admitted selection and creates no record.
* verify_e3_design.py exposes verify(root, manifest) and main(argv), returns JSON-compatible integrity results, and never writes or repairs anything. It validates every declared entry rather than hard-coding23; minimal and23-entry tests create independent fixtures.
* Verifier rejects duplicate JSON keys at every depth, nonstandard constants, unsafe/outside paths, links/reparse points, nonregular files, non-bool permissions, malformed sizes/hashes and missing/changed files. CLI emits only JSON and uses exit0/1. A quiescent filesystem is required; this is not concurrent-adversary isolation.

## Validation

* Real engineering design verification passed:23 entries declared,23 checked, no failures.
* Initial two-module run:29 tests, no failures, four real symlink tests skipped because the host lacks link-creation permission. No elevation requested.
* Added deterministic lstat symlink/reparse rejection fixtures for root, manifest, file and parent-directory checks, plus independent23-entry completeness/failure aggregation.
* Initial editor diagnostics: no errors in the four Python files or this record.
* Final gated run:31 tests in5.167 seconds,27 passed and four real symlink fixtures skipped. Deterministic metadata rejection tests passed.
* Real23-entry design verification passed both immediately before and immediately after the final test run. Commands used Python -B, and no experimental seeds or outputs were generated.

## Follow-on research and clarifying questions

* [ ] Run real symlink fixtures on a host that permits link creation; deterministic metadata checks are not equivalent to actual filesystem coverage.
* [ ] Integrate and validate paid scans, controller/TD/record paths, script padding, ACTION gates, packet consumption and phase permissions in separately authorized work.
* [ ] Freeze source/configuration/tests/analysis/archive and satisfy applicable engineering gates before considering any final target draw.

No unresolved user clarifications. The current implementation is engineering-only
component validation, not an experimental result or a runner authorization.