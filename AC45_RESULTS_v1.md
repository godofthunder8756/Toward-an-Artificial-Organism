# AC45 RESULTS v1 — the family effect is confirmed on a third seed family; the bimodality prediction is falsified

## What ran

`ac45_family.py finals` on the frozen world `ac19` (corruption absent, `reg_rate = 0.0`), seeds
16–23 × histories (0, 1) = 16 individuals, three arms (`two_way`, `two_way_no_repair`,
`two_way_protected`), three family endpoints (`ledger.W_birth`, `ledger.converted`,
`ledger.memory_writes`). Protocol `AC45_PROTOCOL_v1.md` was written and its source list hashed before the
first final seed; the four-check framework was run on the engineering seeds 0–7 first (see §4 of the
protocol).

## Verdict: 5 of 6 gates pass — the family claim is supported, the bimodality prediction is falsified

| gate | result | measured |
| --- | --- | --- |
| G1 family direction & impairment | **PASS** | all three members: median > 0 **and** impaired ≥ 0.75 (in fact 1.0) |
| G2 family significance | **PASS** | 3 of 3 at p = 2.5e-5, the power floor 2/2¹⁶, n = 16 |
| G3 heterogeneity present | **FAIL** | impaired = 1.0 for all three — no unimpaired minority on this seed family |
| G4 protected variant above cut | **PASS** | median(protected − cut) > 0 for all three |
| G5 completeness | **PASS** | 16/16 individuals, no substitution |
| G6 determinism | **PASS** | full re-run reproduces every member exactly |

The **family claim** — repair-maintained register occupancy raises the production/maintenance family —
is supported on its third, disjoint seed family, and more strongly than AC43: the effect is present in
**every individual** (16/16) at the power floor, with no hurt individual (minimum difference +43, where
AC43 recorded −11).

The **bimodality prediction** (AC39 → AC42 → AC43 → AC44: ~88% impaired / 12% unimpaired) is
**falsified on seeds 16–23**: the response is 100% impaired. The "12% unimpaired" minority was
seed-family-specific, not a stable feature of the world.

## The numbers (fresh seeds 16–23)

| endpoint | median Δ | mean Δ | impaired | p | min Δ | protected − cut (median) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `W_birth` | 165.5 | 144.0 | 1.000 | 2.5e-5 | +43.0 | 174.5 |
| `converted` | 463.0 | 448.8 | 1.000 | 2.5e-5 | +293.0 | 569.5 |
| `memory_writes` | 1233.0 | 1259.3 | 1.000 | 2.5e-5 | +1035.0 | 2168.0 |

All three endpoints hit the exact sign-flip test's power floor: every one of the 16 individuals is
impaired on every member, so the observed mean difference is the extreme of the null distribution.

## Reading: a fourth instance of the seed-transfer lesson, now for the impaired fraction itself

AC39's lesson — engineering statistics do not transfer to final seeds — has now been observed for the
**impaired fraction**, not just the p-value. The impaired fraction was 0.88 on engineering seeds (0–7,
AC42), 0.875 on AC43's finals (8–15), and 1.0 on AC45's finals (16–23). The heterogeneity that made a
"bimodal metabolic response" the right description on two seed families is absent on the third. The
*effect* is stable and uniform across all three families; the *shape* (heterogeneous vs uniform) is
not stable.

## A gate-shape self-correction, recorded not retracted

G3 ("heterogeneity present: 0 < impaired < 1") was carried over from AC43's G4, where it passed at
0.875. It conflated a **prediction about the response's shape** (AC39's bimodality) with the **family
rule** (G1 + G2), which concerns only direction and impairment. The handoff's family rule specified
`impaired ≥ 0.75` — a lower bound — with no upper bound; G3 added the upper bound and it is the gate
that failed. This is AC16's lesson in miniature: classify the claim before choosing the gate, and keep
a prediction-about-shape out of the falsifying gate set. The failure is **recorded, not re-run, and not
reclassified**: the study stands with 5/6 gates, G3 falsified, and the correction is logged here and in
the test suite, which asserts G3 is False so a future change is caught rather than absorbed.

## Why the family of three (restated from the protocol)

`spent_e` and `spent_m` are total-spending sums, tied linearly to the production quantities by AC4's
conservation law (`spent_m == writes + 4*(W_birth + C_birth) + 2*B_birth`; `b.energy == E + 8*converted −
spent_e`), so they are double counts excluded from the family. `deposits` is 100% impaired (no
heterogeneity) and was excluded for that reason. The three members are independent
production/maintenance endpoints: catalyst births, energy conversion, and memory renewal.

## Verification performed

- `audit_ac45.py` — PASS: recomputed gates match the frozen record, 4 source hashes unchanged; reports
  G3 FAILED as recorded.
- `replay_ac45.py` — PASS: two individuals × three endpoints reproduce exactly in a fresh process.
- `test_ac45.py` — 13 tests OK: family rule passes, G3 falsification pinned, hashes and preflight, seed
  disjointness, claim discipline.

## What this does and does not establish

- **Establishes**: repair-maintained register occupancy raises all three production/maintenance
  endpoints, in every individual, on a third disjoint seed family — the family claim. And that the
  bimodality of the metabolic response is seed-family-specific (88% on two families, absent on the
  third).
- **Does not establish**: a stable bimodality (falsified); any claim about experience, understanding or
  life; autopoiesis or closure (AC14 remains a negative result); survival (AC34). The endpoints are
  births, conversions and writes.

## Next

The family claim now stands on three seed families. The bimodality prediction is recorded as falsified
and should not be re-asserted. A successor, if one is wanted, could register the family claim **without**
the heterogeneity gate — which was a prediction about response shape, not part of the family rule — on a
fourth seed family, to obtain an all-gates-pass study. Alternatively the line can turn to the still-open
AC37 drain mechanism.
