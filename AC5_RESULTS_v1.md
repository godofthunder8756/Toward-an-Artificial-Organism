# AC5: all-or-nothing commitment revision fails viability

2026-09-15. Negative engineering result, preserved without tuning. Goal active.

## Result

The compact controller and paid commitment mutation work as implemented, but
the proposed adaptive strategy is not viable. Only1/8 adaptive individuals
completed8192 ticks, compared with8/8 frozen controls. Protected-program learning
has identical body endpoints and event ledgers to the adaptive arm for every
seed, so a protected acquired program does not rescue this failure.

| Arm | Completions | Mean active fraction | Mean B births during support |
| --- | ---: | ---: | ---: |
| Adaptive | 1/8 | .536 | 16.375 |
| Frozen | 8/8 | 1.000 | 425.250 |
| Random feedback | 0/8 | .089 | 0 |
| Phase-informed | 2/8 | .829 | 0 |
| Protected program | 1/8 | .536 | 16.375 |

Every endpoint preserves100% structural program accuracy (excluding the mutable
enabled bit). The adaptive strategy fails completion, activity, viable
relinquishment and reacquisition criteria. Lower B production and structural
integrity pass only their narrow checks; neither converts this into adaptive
success. Dead individuals consume fewer resources too.

Only half of adaptive individuals were active through the final support window.
Mean active-and-commitment-on fraction after support removal was.166, far below
the.8 criterion. Frozen control shows that the environment remains viable under
the original maintenance commitment. Its success is not evidence of learning.

## What this changes

The integrated compact126-bit controller is a working alternative representation
at these conditions. The fixed controller maintains itself and the W/C/B system;
no broader robustness improvement over AC4 is claimed from this differently
encoded acquired state.

An exploration law that temporarily abandons the entire enclosure is too risky.
Real outward crossings correctly signal loss of retention, but they may arrive
after many links have expired. Resuming production replaces only one accessible
segment per action while W/C can continue to escape. This explanation is
consistent with the laws and controls; a full causal mediation analysis remains
undone. All six failed informed controls terminate after support withdrawal
(active ticks6240–6492); even exact current-phase knowledge does not ensure
reconstruction fast enough. Advance notice was not provided to that control.

The next design should test bounded omission of a local component while preserving
enough organization to recover. Distinguish the value of learning from the cost
and reversibility of the intervention used to learn. Complete relinquishment of
an essential, slowly rebuilt enclosure is not automatically an appropriate test
of adaptability when support can vanish without warning.

This is a research decision, not a reason to relax the frozen AC5 gates. A new
version must declare its different probe and new criteria before outcomes.
Useful contrasts include local bounded probe, global probe, frozen maintenance,
protected learner and external support with declared withdrawal conditions.
Local probing may discover a substituted dependency without requiring collapse
of the whole boundary. It remains an untested hypothesis.

## Mechanism and verification

Four integrated tests verify paid replica updates, feedback from actual outward
crossing, no direct phase signal in the adaptive arm, protected-state rejection,
whole-state erasure, capacity rejection and short replay. Existing compact
program tests cover12288 equivalence comparisons.

All40 declared rows are retained. The same-author audit verifies source hashes,
incremental-log agreement, rectangular coverage, energy/fuel/material balances,
phase totals and five exact seed200 reruns. Adaptive/protected body endpoint
hashes and ledgers additionally match across all eight seeds. Protected control
stores an explicit external trace copy; only its program is read. This privilege
is not present in adaptive or frozen individuals.

Learning uses one experience-dependent bit with an engineered directional law,
supplied crossing sensor and random exploration. There is no discovery of a
new need, intrinsic normativity, rich developmental identity or full autopoiesis.
The failures are an implemented and tested limitation of this strategy, not a
proof that adaptation in a self-maintained architecture is impossible.

[Protocol](AC5_PROTOCOL_v1.md), [model](ac5.py), [tests](test_ac5.py),
[data](ac5_results_v1/results.json), [audit](ac5_results_v1/audit.json),
[audit source](audit_ac5.py). All runs/audits are terminal; preserve earlier freezes.
