---
title: E3 isolated meter implementation evidence
description: Contract research, component API, validation, and limitations for the engineering-only meter
ms.date: 2026-09-10
---

## Status and scope

Complete. Changes are limited to e3/meter.py, test_e3_meter.py, and this
tracking document. No worker, E3 seed, final target, physical module, or frozen
contract is changed or executed.

## Research questions

* What current packed-state capabilities and frozen admission rules apply?
* How are sourcewise bounds, paid gates, shutdown, and deposits distinguished?
* Which static witnesses qualify METER128 and the mandatory-versus-optional TD case?
* Which isolated tests verify the API without claiming full VM conformance?

## Findings and evidence

* e3/state.py supplies one authoritative 276-byte state and typed E/P accessors.
  Meter work must not read acquired RAM or retain a decoded state mirror.
* E3_OPERATION_CONTRACT_v0_3.md requires componentwise c+L+T+rho admission,
  METER128 before optional comparison, debit before deposits, and absorbing E=0.
* E3_CONTROL_CONTRACT_v0_6.md prepays two CONTROL256 budgets; bounds are
  recomputed current-operation values, never escrow or spent-resource fields.
* E3_INTEGRATION_DECISION_v0_11.md permits isolated engineering after snapshot
  verification, not final-target draws or confirmatory H2 execution.
* .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md,
  "Gates, branches, kernels and liveness", restricts quote arguments to public
  configuration and paid current scratch; no durable admission flag is permitted.
* .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md,
  "TICK with no CONTROL envelope", identifies passive support before preflight
  and ignored support at E=0. Later TICK I/O, transport and living remain paid.
* .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md,
  "Exact local and future remainder witnesses", supplies routed TERMINAL
  minimum 904/four per source and optional TD 217/two per source.
* .copilot-tracking/reviews/2026-09-10/e3-integration-review.md,
  "Static machine acceptance and unchanged precision", accepts METER128 as
  an abstract primitive, not a lowered native-code proof.
* .copilot-tracking/reviews/2026-09-10/e3-b06-review.md, AN-001, protects
  mandatory clearing, not optional TD. The test derives all twenty conditioner
  vectors from domain and lane hubs, reproduces admitted domains
  0,1,2,3,4,5,6,7,9,11,13 and remaining material (4,5,4,6). TD rejects after its
  paid gate; mandatory retirement remains funded and leaves (0,1,0,2).

## API and implementation

* `Cost(energy=0, material=(0,0,0,0))`, also named `Bound`, is frozen/slotted
  with a four-source immutable tuple. All components are built-in integers
  within 0..2147483647; booleans, negatives, coercions and overflow are errors.
* `add_cost(left, right)` and `sub_cost(left, right)` validate componentwise
  arithmetic; subtraction cannot create negative credit.
* `floor_quote(c, local_remainder=ZERO, public_tail=ZERO, residue=1)` computes
  checked c+L+T+rho without reserving or debiting anything.
* `require_cost(state, c, local_remainder=ZERO, public_tail=ZERO, residue=1)`
  is a pure current-stock predicate. Energy must preserve a positive residue;
  source material may meet equality. It is not a free interpreted-policy sensor.
* `gate(state, c, local_remainder=ZERO, public_tail=ZERO, minimum_exit=None,
  residue=1)` first checks 128+minimum_exit+T+rho, where omitted minimum_exit
  means L. Failure sinks only E. Otherwise it pays 128 and checks c+L+T+rho.
  The immutable `GateResult` exposes paid/enough/shutdown_loss and derived status.
  No optional work, retirement, flags, scratch clearing or implicit close occurs.
* `debit(state, c, local_remainder=ZERO, public_tail=ZERO, residue=1)` validates
  then debits packed E/P before work/output. It returns only actual paid cost,
  not a balance. Unaffordable debit raises `InsufficientResources` unchanged.
  No repeated gate fee, escrow, prepayment or implicit physical shutdown occurs.
* `deposit(state, packet, permitted=..., energy_cap=65535,
  material_caps=(255,255,255,255))` implements the already-paid current-gate
  continuation. Packets fit E16/P8 and their explicit permitted bounds. Results
  contain accepted/cap-overflow/ignored flows, not stock snapshots or receipts.
* `debit_and_deposit(state, c, packet, L, T, permitted=..., ...)` validates
  both commands before mutation, debits before accepting yield, and returns
  immutable actual paid cost and flows. Yield cannot self-fund the debit.
* `passive_grant(state, packet, permitted=..., ...)` is the TICK-only
  preflight exception. Initial E=0 ignores the whole grant without revival.
* `canonical_activation(energy, material, energy_cap=..., material_caps=...)`
  accepts no old state and constructs a fresh powered canonical reset image.

Names above abbreviate arguments for readability; `minimum_exit`, deposit
configuration/permissions, and activation caps are keyword-only in the code.
Caps are caller-supplied and independent of any concurrently implemented physical
module. Meter imports only state constants/codecs and standard-library types.

No instance owns resources, tails, acquired fields, logs or operation history.
The caller computes unknown-address maxima separately for each source, excludes
already-paid work from L, keeps T public, consumes results within the owning
operation, and executes actual memory writes/clears separately after debiting.

## Validation results

* All 23 entries in E3_DESIGN_FREEZE_v0_11.json matched both byte count and
  SHA256 before implementation.
* The selected Python 3.13 interpreter ran `-B -m unittest test_e3_meter -v`:
  29 tests passed in 0.028 seconds on the successful validation run.
* Pylance `textDocument/diagnostic` returned no diagnostics for either Python
  file. The editor error check was also clean for both files and this document.
* Fixtures check exact resource-only snapshot deltas, componentwise energy and
  material edges, overflow validation before mutation, failed minima, nested
  fee/cleanup floors, distinct minimum/body remainders, two prepaid CONTROL256
  charges, nonprepaid loop bounds, caps/flow conservation, shutdown/activation,
  no acquired-RAM/snapshot reads, and resource-only snapshot replay.
* Observer fixtures keep audit lists outside the meter and never feed those
  lists back into any operation. No test produces experiment or archive output.

The initial validation exposed a fixture exception mismatch (tuple method lookup
raises AttributeError rather than the assignment TypeError being tested) and
Pylance fixed-size tuple errors (`reportAssignmentType`/`reportArgumentType`).
Use `operator.setitem` for the intentional invalid assignment and explicit
four-element tuples or a typed fixture helper; do not weaken the API's tuple
shape or suppress its diagnostics. Both issues were corrected and revalidated.

## Limitations and next checks

METER128 is an abstract tariff, not a native instruction trace, hardware energy
claim, VM, or process-isolation proof. Typed stock updates are validation-atomic
in the selected fault-free operation window, not synchronized across threads.
Python host code can bypass normal encapsulation; this component is trusted
host machinery, not a policy sandbox or extra acquired-resource ledger.

* [ ] Integrate pure G/ROM quotes with paid scratch arguments and actual linked
  instruction sites without adding state or changing fees.
* [ ] Validate packet provenance, one-shot yield use, scalar counts, admission
  ordering, and maximum accepted-material transport before any live output.
* [ ] Validate real memory retirement, S boundaries, process capabilities and
  full VM conformance separately; accounting tests do not execute those services.

These are later integration checks, not missing requirements for this isolated
component. No additional research or user clarification blocks this handoff.

## Clarifying questions

None currently required for this isolated component.