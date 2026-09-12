---
title: E3 B03 physical-contract selection
description: Design-only decisions, revised service bounds, and remaining physical-contract blockers
ms.date: 2026-09-10
status: Complete - selection only; B03 partial
---

## Scope and questions

Select E3_PHYSICAL_CONTRACT_v0_4.md without code, simulation, a design freeze,
or changes to existing contracts. Resolve finite placement, material conditioning,
twenty paid ages, live lapse, finite support and source-prefix accounting.
Keep B04-B07 unresolved where evidence is missing.

## Evidence

* E3_OPERATION_CONTRACT_v0_3.md: tariffs, METADATA services, CONTROL256,
  componentwise tails, typed resources, event order and scratch partitions.
* E3_STATE_CONTRACT_v0_2.md: exact state offsets, domain-age capacity,
  vulnerable routing/policy, reset and planned denominators.
* .copilot-tracking/research/subagents/2026-09-10/e3-b03-feasibility.md:
  finite tree candidate, all-mandatory conditioning limitation, existing
  affordability witness and unresolved H2 housekeeping subsidy.

## Selected decisions

E3_PHYSICAL_CONTRACT_v0_4.md is the sole selected contract. The prior feasibility
record remains unchanged; no alternative root contract, code or simulation was
created. Only this short record and that root contract are authorized outputs.

* Retain the 25-vertex tree, exact 2,208-bit persistent map, twenty declared
  ages, source-local pools capped at 255 and E capped at 65,535.
* Select sacrificial environmental conditioning: generic material lowers future
  hazard without payload reads/restoration. No RAM-refresh interpretation,
  hidden true age, inaccessible-reserve access or fourth agent action is allowed.
* Select two ten-age services, each 952 energy and five material per source.
  Eight explicit ALUs per word include field extraction, shift, comparison,
  saturation and masking. A full increment pass has forty reads/forty writes;
  full conditioning adds forty reset writes. The candidate CONTROL budget is
  232 per ten-age service, not 432 in one over-cap twenty-age service.
* Each of twenty automatic conditioner services costs 520 energy on rejection
  or 552 on admission, with a three-material source-specific admitted body.
  Complete upkeep is 12,304+32n energy, from ten material per source at n=0
  to 25 at n=20. n is an offline count, never worker state.
* HS-AC is the primary externally supported always-conditioned reference,
  explicitly not live lapse or autonomy. LL-EVAL13 uses the same process and
  paid clock, reducing only H1 g to thirteen per source. At tick seventeen
  it admits domains 0,1,5,7 and remains live; later admission ticks admit only
  domain 1. No favorable fault draw or extra storage is needed for this
  financial prefix. It is not learned selection or the H2 scarce condition.
* All fault probabilities use current ages after every conditioner, before
  simultaneous faults including age-lane faults. Recovery retains 128 wearing
  ticks at fully conditioned h=0.001, then p=0.1 challenge and all 261 wearing
  H1 ticks. Q/routing/metadata are never silently protected.
* FULL-SOURCE-ENTRY explicitly removes/logs old stocks and supplies full new
  resources to eligible live reference bodies; paid ISOLATE follows. No dead
  historical worker is revived. The extra pre-H1 boundary is selected openly,
  not inferred from empty-looking RAM. Ordinary global H1 support can saturate
  refill/sham/external-funding contrasts; their B05 product remains unresolved.

## Revised bounds and evidence

Offer 30,000 energy per tick, equally to repetition/block. Named material
offers per source and block maximum energy debits, excluding one leakage, are:

* HS-ACQUIRE: g=48, energy 17,559.
* HS-DEVELOP and HS-H2-REFERENCE: g=66, energy 29,138.
* HS-RECOVER: g=47, energy 26,084; no query admissions, but RESPONSE still runs.
* HS-H1: g=28, energy 18,339.
* LL-EVAL13 H1: g=13, energy at most 18,279; tick seventeen at most 17,767.

New full upkeep is 12,944 energy, versus the old candidate's 1,432: +11,512,
plus forty additional maximum grant-transport energy in each high-support tick.
The old 20,000 energy offer and low-g tables do not prove these bounds.
Full conditioned H1 costs at most 4,784,234 block energy or 3,761,114 repetition
energy before leakage/boundaries, and 7,303 material per source with leakage.
The updated all-conditioned H2 no-code envelope is 20,481 per source.

Literal scalar arithmetic was checked without an E3 worker, random draws,
program implementation or simulation. The root contains the operation and
source-prefix derivations. Instruction budgets are not expanded/static runtime
traces; no such conformance or empirical test is reported as passed.

## Uncompleted research and closure checklist

* [ ] B03: expand/check the 22 service CONTROL/register traces and exact quotes;
  retain partial status until conformance, not just capacity, is established.
* [ ] B04: returns, signed bounds, sensors, policies, metadata/refresh and grids.
* [ ] B05: full products, boundary/refill saturation controls, calendars,
  source opportunities, indexing and row counts, including LL-EVAL13 panels.
* [ ] B06: H2 scarcity and viable selective spending, positive O-write
  denominators, H1/adaptive headroom and dependent-output erasure precision.
* [ ] B07: ownership/noninterference and operational review; production tests
  require later implementation authorization. No design freeze is authorized.

Frozen bookkeeping still saves 48 material overall per updated admission tick,
more than maximal block correction; dropped TD remains legal. No favorable H2
g is selected to conceal this obstacle. No user clarification is required.