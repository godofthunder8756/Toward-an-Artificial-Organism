# SUB-A0 engineering errata v2: reclassification and two arm defects

2026-10-04. This errata is additive. It does not edit the original execution source, manifest, traces,
checkpoints, results, [engineering review](SUB_A0_ENGINEERING_REVIEW_v1.md) or
[errata v1](SUB_A0_ENGINEERING_ERRATA_v1.md). Nothing was rerun or retrained to
write it. All numbers come from the saved records in
[sub_a0_engineering_v1/](sub_a0_engineering_v1/).

## E1. Outcome reclassification: INVALID, not NEGATIVE

The review labelled the run `ENGINEERING_STOP / REGIME_DOES_NOT_REQUIRE_MAINTENANCE`
and `CAPACITY_PROBE_UNIDENTIFIABLE`. Under the four-way taxonomy now in use
(INVALID / NEGATIVE / POSITIVE / UNRESOLVED), the correct label is:

**INVALID: failed positive control.**

- No-write kept whole-horizon accuracy at 1.000000. That arm is the negative
  control for maintenance. Because it did not degrade, the regime put no pressure
  on maintenance, and no allocation contrast or repair-capacity contrast could be
  identified.
- The A0 trace confirms this. With no writes, the task-bank |mean| fell from 4.4427
  (tick 1) to 1.2169 (tick 1,024), but no readout sign flipped. Shrinkage cut the
  margin and never crossed zero. The damage timescale was longer than the 1,024-tick
  horizon.
- All six capacity probes read `before = immediate = after = 1.0`. The
  probe perturbation set one replica of a triplet to zero. The other two replicas
  keep the same sign, so the mean readout cannot flip. The probe was therefore
  ceiling-limited by construction, not only empirically.
- Allocation enrichment D = 0.00099 (registered margin 0.10) was measured in a
  regime where maintenance was not needed. It is **not interpretable** as evidence
  for or against damage-induced allocation.

**Citation rule.** Do not cite SUB-A0 engineering as evidence against
learned self-maintenance allocation, against priorities arising from dependence,
or against the feasibility of learned repair. What it does establish:

1. the infrastructure works: 56 tests, replay without retraining, an independent
   tick-level audit, and the documented hash-definition fix;
2. the A0 fault law over 1,024 ticks does not make maintenance load-bearing for a
   3-replica mean-thresholded table acquired at |T| = 4.449.

## E2. Defect: the "immortal reference" was the SHAM arm

In [run.py](sub_a0_v1/run.py), `evaluate` applies damage only when
`arm not in ("sham", "immortal")`, and no other line treats `immortal`
differently. So both arms ran the candidate with no faults **and** with live
writes. Their saved records are identical:

| Arm | A | Accuracy | writes_R | writes_T | trace_sha256 (LF) |
| --- | ---: | ---: | ---: | ---: | --- |
| sham | 0.0625242730995589 | 1.0 | 41,102 | 221,042 | `2bee3ae9…dfcad` |
| immortal | 0.0625242730995589 | 1.0 | 41,102 | 221,042 | `2bee3ae9…dfcad` |

The physical trace files also have the same SHA-256 (`761871EE…7224`).
A0 therefore had **no independent no-fault, no-write ceiling arm**. The review's
row "Immortal reference" duplicates SHAM. This does not change any reported
number. It removes one claimed control. All future runs must implement IMMORTAL as
no faults and no writes, and test that it differs from SHAM.

## E3. Defect: the EXTERNAL arm's write physics did not match the candidate's

The `external_code` arm moved each selected destination straight to the
live triplet median (`delta = target - value`, no bound). It chose among all 894
destinations by |delta|. The candidate is limited to `|delta| = |0.05 tanh(.)| < 0.05`
per write. At |T| = 4.449, the external arm could restore an erased replica in one
write, while the candidate needed about 89 writes. So the external arm was a
privileged-physics reference, not a matched positive control. A0-cal adds a
matched, bounded external repairer
([protocol](SUB_A0_CAL_PROTOCOL_v1.md)) and keeps the A0 jump rule only as a
labelled reference.

## E4. Disclosed confound, carried forward: R/T scale

Acquisition (Adam, lr 0.1, 128 BCE steps starting from zero) is deterministic in
magnitude. Every acquired task coefficient for every seed is exactly
±4.449178695678711; a regression test verifies this. Performing coefficients
averaged |0.278| after development. Under the shared absolute fault law, any dose
that degrades T will degrade R much faster in relative terms. The review already
disclosed this. It matters more after recalibration, because a stronger dose
widens the relative gap. It is addressed prospectively, not by changing the
substrate. The [validity gate](SUB_A0_VALIDITY_GATE_v1.json) and the
[re-test proposal](SUB_A0_RETEST_PROPOSAL_v1.md) pre-register a
disagreement-proportional allocator as the reduction rival.

## Scope

- No scientific endpoint, threshold, seed set or stored artifact changes.
- The registered A0 allocation endpoint (A > 0.10, D > 0.10, 23/32) is unchanged.
- Phase III-B verdict B and A6 UNRESOLVED are untouched.
- No Phase A license existed before this errata, and none follows from it.
