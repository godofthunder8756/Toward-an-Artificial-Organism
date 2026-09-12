---
title: E3 physical component implementation evidence
description: Research and deterministic component validation for the engineering-only physical layer
ms.date: 2026-09-10
status: Complete - deterministic component scope only
---

## Scope and questions

Implement only e3/physical.py and test_e3_physical.py, with this optional
tracking document. Verify the frozen placement, costs, age storage, simultaneous
explicit-draw faults, typed leakage, injury maps, and absorbing dead-state
behavior against the actual State API. No stochastic experiment or final target
draw is authorized. Component checks do not certify paid upkeep or a worker VM.

## Evidence collected

* e3/state.py stores exactly one 276-byte buffer. Its trusted physics lane
  methods include reserve and exclude typed reservoirs; snapshots copy raw bits.
* E3_PHYSICAL_CONTRACT_v0_4.md selects the 25-vertex tree, 1,080 RAM lanes,
  twenty domains, storage-domain age hazards, typed leakage, and three lesions.
* E3_OPERATION_CONTRACT_v0_3.md fixes read energy 3+7d and write energy
  6+8d+material distance, with one material at the assigned source per write.
* E3_INTERFACE_CONTRACT_v0_9.md specifies 1,104 placement rows and external
  physics ownership. Physical draw frames are not worker protocol frames.
* E3_INTEGRATION_DECISION_v0_11.md permits engineering implementation after
  verifying the design snapshot, but prohibits final execution.

## Decisions

Use only inherited immutable placement tables and explicit integer draws.
Represent each of the 3,160 fault slots by an integer in 0..9,999. For stored
age a, compare flip draws with 10(a+1) and erasure draws with a. A temporary
pre-fault state copy determines every age and symbol; no copy survives in the
module or returned observer ledger. Age access helpers are low-level codecs,
not paid increment/conditioning services.

The selected configuration has no instance fields or constructor inputs.
Its class-level tuples cover all 1,104 positions, with 1,080 unique RAM lanes,
948 accessible lanes, 132 reserve lanes, and 24 typed reservoir positions.
Each hub owns twenty code lanes, 192 Q lanes, 58 other auxiliary lanes,
270 total RAM lanes. Each age lane uses storage domain 5j+4 at its own hub,
not the domain whose age word it helps encode.

Placement rows are logical values for the v0.9 eight-byte layout, not an
implemented binary codec. E uses hub sentinel 255 to denote X and domain 4;
Pj uses hub j and domain 5j+4. Typed reservoir write sources are None. Both
typed and reserve lanes reject agent read/write quotes, while reserve remains
included in trusted faults and whole-hub lesions.

Fault slots follow ascending global RAM lane index, skip reservoirs, and use
code_flip/code_erase or aux_bit0/aux_bit1/aux_erase in that order. FaultFrame
clones list inputs into checked tuples. apply_faults revalidates the complete
frame before any mutation, including at E=0. There is no frame seed, root,
label, historical image, worker-packet codec, or protected zero-wear selector.

At E>0, RAM changes precede typed min(stock,1) leakage; the E sink is last.
E=0 skips all physical transitions, including injuries. Corrupt diagnostic
dead flags do not override E. No output, cleanup, age increment, condition
reset, status write, replenishment, or resume is implied by a physics call.

## Implemented API and compatibility

All new imports are directly from e3.physical; e3/__init__.py is unchanged.

* PhysicalConfig, LanePlacement, DomainPlacement, DEFAULT_CONFIG: inherited maps
* lane_read_cost, lane_write_cost, write_quote, ResourceQuote: informational
  lane tariffs and bounded sourcewise write-multiset quotes
* age_lanes, read_age, write_age: explicit low-level current-state age codecs
* conditioning_vector, conditioning_quote: body-only dues and two age writes
* fault_thresholds, FAULT_SLOTS, fault_slot_indices, FaultFrame: exact discrete
  threshold counts and indexed current-physics inputs
* apply_faults: simultaneous RAM faults and typed leakage
* apply_primary_lesion: 32 code sites at layers three and four across all blocks
* apply_hub_lesion: one hub's code, auxiliary RAM, reserve, whole Pj, and floor(E/2)
* apply_global_resource_injury: floor-halving losses from E and each P, no RAM writes
* LossLedger: nonnegative E/P losses, negative delta properties, net changed code
  and auxiliary lanes, and net changed RAM bits; observer-only, not paid spending

The implementation depends only on the standard library and the actual State
codec. It calls State.read_bits/write_bits, snapshot, the reserve-inclusive
trusted physics lane methods, and typed energy/material accessors. It introduces
no NumPy dependency, environment integration, package re-export, or sibling edit.

## Validation

* Verified all 23 entries of E3_DESIGN_FREEZE_v0_11.json by byte size and SHA-256
  before implementation and after tests. Final target permission remains false.
* Python 3.13 selected by the editor ran `-B -m unittest test_e3_physical`:
  25 tests passed in the final run (1.748 seconds). No bytecode output requested.
* Independent per-bit reference calculations cover every RAM lane, original
  stored ages, erasure precedence, reserve exposure, exact resource deltas, and
  simultaneous age corruption. Fixed arithmetic fixtures use no PRNG.
* Enumerated all 10,000 possible draw values for each of sixteen ages to check
  exact rational threshold counts. Separate transition tests cover equality
  boundaries, auxiliary bit purposes, and all-zero/all-9,999 draw arrays.
* Checked read/write energy 17/23 for code and 10/14 for auxiliary RAM; sourcewise
  quotes preserve repeated addresses. Full conditioner bodies sum to fifteen
  material per source, plus ten per source from age writes, totaling twenty-five.
* Checked immutable maps/frames, complete malformed-frame rejection before state
  mutation, no retained state snapshots in observer results, all three injury
  maps, odd-stock floor losses, and absorbing dead/final-leak-death behavior.
* Editor diagnostics report no errors in either new Python file. Pylance file
  diagnostics returned empty item lists. One test list needed a type annotation;
  it was corrected and the tests and diagnostics rerun successfully.
* Git status was unavailable because this workspace is not a Git repository.
  Only the two new Python files and this permitted tracking note were edited.

These are component tests, not stochastic experiments, paid instruction traces,
full package regression tests, implementation conformance, scientific gate
passes, a source/configuration freeze, or final hypothesis runs.

## Remaining research and clarification

No user clarification is required. The following work remains outside this scope:

* [ ] Private HMAC uniform-10,000 generation with twelve-coordinate provenance
  and per-purpose independence checks
* [ ] Paid AGE/CONDITION/READ2/WRITE2 execution, sourcewise admission, and static
  instruction/scratch conformance without exposing these host codecs to workers
* [ ] Independent replay and original observer archive integration, including
  loss-flow direction and placement-row byte serialization
* [ ] Lifecycle/capability isolation, sibling regression suite, and broader
  end-to-end technical validation before any separately authorized engineering run