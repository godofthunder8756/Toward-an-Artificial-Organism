# AC9 allocated memory: implemented physical prerequisite

2026-09-15. The memory primitive is implemented and tested; integrated organism
growth has not been run. No developmental autonomy result is claimed yet.

## Implemented state and reactions

Two regions each have two potential entry slots. Capacity/geometry are supplied.
An entry contains valid/key/value bits with seven replicas each. Every physical
replica has a lifetime; zero lifetime means absent matter. No key-address cache,
occupancy bitmap or original value is retained outside these arrays.

Depositing an entry consumes21 precursor and21 energy, binds21 units of material
and requires at least three available W at eight writes/W, cap32. Local sensory
activation and available W determine which region can receive deposition; the
primitive reads no developmental-history label. It receives a key/value from
the calling learning event, whose outcome derivation still requires integration.

Every replica expires after64 ticks unless replaced. Renewal uses only current
majority among surviving replicas, including key and validity information. It
replaces near-expiry, absent or disagreeing replicas at1M+1E each. Every occupied
replacement emits one waste unit; every new replica adds one bound unit.
Expiry emits one waste unit and clears the former bit. Absent sites do not
receive corruption or consume repair material.

An entry is unreadable when fewer than four replicas of any field remain or
majority ties. Corrupted validity/key can hide an entry; no protected target
reconstructs it. Conflicting decoded values for a key return no answer.
This decoding law is supplied, not learned.

## Five passing mechanism tests

- Empty sites remain physically absent under corruption and renewal.
- Local deposition pays all21 replica costs and creates demand only in its region.
- Insufficient energy/material/catalytic capacity rejects the transaction exactly.
- Majority corruption changes the retrieved value; renewal preserves that changed
  value rather than restoring the original. Expiry erases all state.
- Identical entries deposited in different regions respond differently to the
  same later region0-only renewal: region0 retains its entry and region1 loses it.

The last test is a mechanism assay with externally supplied renewal/resources,
not autonomous regional maintenance by the AC4 controller. It must not be
presented as the full proposed history-dependent organism experiment.

## Bootstrap issue found before integration

The [reference timing probe](AC9_BOOTSTRAP_REFERENCE_v1.json) runs the existing
AC7 body and records first productive contact times:24–32 ticks across its eight
seeds. Initial unrenewed regional W lifetimes are32/48/64. At tick32 only two
would remain, insufficient for a21-write atomic entry. This exposes a bootstrap
constraint if unused regions stop receiving W production.

These are AC7 contact times, not predictions for AC9: its smaller occupied state
and extra deposition cost will change the trajectory. The initial endowment
must nevertheless be accounted for; silently replenishing an empty region would
manufacture the purported developmental capacity.

## Next integrated work

Use this memory as the actual route store, searched from live entry contents.
Remove the corresponding unused always-allocated payload regions. Regional W
production and renewal decisions must follow actual demand. Preserve a vulnerable
core controller and paid W/C/B maintenance. Caller must charge the enclosing
action's living cost and share its write capacity, so deposition cannot acquire
an extra free action. Extend whole-body accounting and erasure to these arrays.

Choose and declare bootstrap semantics before outcomes: early growth supported
by a finite endowment, paid seeding from existing catalysts, or an explicit
multi-action deposition protocol. Each is a different mechanism requiring tests.
Do not pick among them after seeing which seeds fail without versioning the test.
The design's no-growth, inert-entry, fixed-allocation, stateless and protected
controls remain required for a broad interpretation.

[Source](ac9_memory.py), [tests](test_ac9_memory.py),
[reference probe](probe_ac9_bootstrap.py), [design](AC9_DEVELOPMENTAL_DESIGN_v0_1.md).
Run `py -3.12-arm64 -B -m unittest -v test_ac9_memory` for the mechanism tests.
