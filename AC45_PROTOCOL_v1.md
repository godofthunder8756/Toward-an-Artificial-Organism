# AC45 PROTOCOL v1 — registered before the first final seed

**Endorsement.** This protocol was written and its source list hashed **before** any final seed was run.
The result directory is created with `mkdir(exist_ok=False)`, so a frozen directory can never be
overwritten. A self-declared defect elsewhere causes a hash mismatch; none is declared here.

## 1. The claim, in the form its own shape permits

*Repair-maintained register occupancy raises the organism's **production and maintenance family** of
endpoints over a run, relative to its absence, under corruption absent.*

The endpoint is not one quantity but a **family of three**:

| member | what it counts |
| --- | --- |
| `ledger.W_birth` | W-region births (repair-catalyst production) |
| `ledger.converted` | fuel → energy conversion (metabolic throughput) |
| `ledger.memory_writes` | memory renewal writes (maintenance) |

AC44 (engineering) showed the effect is endpoint-general at AC43's final seeds (8–15): six of six
quantities rise. But the gate outcome is endpoint-dependent — `spent_m` has the same 87.5% impaired
fraction as `W_birth` yet p = 0.0127, above the 0.01 bar. A single endpoint is a bet the survey cannot
hedge; a family with a declared rule is the honest shape of the claim.

**Why these three and not the other candidates.** The family members are the *production/maintenance*
endpoints, each measured directly and not a function of the others:

- `spent_e` and `spent_m` are **total-spending sums**. AC4's frozen conservation law ties them linearly
  to the production quantities — `spent_m == writes + 4*(W_birth + C_birth) + 2*B_birth`, and the energy
  balance is `b.energy == E + 8*converted − spent_e` — so they carry no evidence beyond the production
  endpoints and are excluded as double counts. (`spent_e` also clears p ≤ 0.001 on final seeds, at
  0.000895, but it is a spending aggregate, not a production output; this is stated here rather than
  hidden.)
- `deposits` is **100% impaired** — no heterogeneity — so it fails the bimodality requirement the claim
  carries (see §3, G3).
- `productivity_kept` is **inverted** (the cut arm scores higher), already flagged by AC42.

## 2. Design

| item | declared value |
| --- | --- |
| capable arm | `two_way` |
| cut arm | `two_way_no_repair` |
| second capable variant | `two_way_protected` (gate G4 only) |
| **corruption** | **absent** — `reg_rate = 0.0`, so AC14's integrity channel is off by construction |
| endpoints | `ledger.W_birth`, `ledger.converted`, `ledger.memory_writes` (the family) |
| individuals | **seeds 16–23 × histories (0, 1) = 16** |
| freshness | engineering used seeds 0–7; AC43 finals used 8–15; these 16 are disjoint from both |
| runner | `ac45_family.py` (`main`), result directory `ac45_results_v1/` |
| sources | hashed into `pre_run_snapshot.json` before the first individual |

## 3. Declared gates — all six must pass

| gate | criterion | declared from |
| --- | --- | --- |
| **G1 family direction & impairment** | **every** member: median paired difference > 0 **and** impaired fraction ≥ 0.75 | AC44 measured 87.5% impaired for all three on final seeds |
| **G2 family significance** | **at least 2 of 3** members resolve at **p ≤ 0.01** on the exact sign-flip test (n = 16, power floor 2/2¹⁶ = 3.05e-5) | AC44's final-seed p: 0.000105, 0.000630, 0.000290 — all ≤ 0.01, but the rule tolerates one member degrading (the `spent_m` lesson) |
| **G3 heterogeneity present** | **every** member: 0 < impaired fraction < 1 | the bimodality is part of the claim; a uniformity claim is not permitted to pass |
| **G4 protected variant above cut** | **every** member: median(`protected` − `cut`) > 0 | a second, independently-degraded capable arm must sit above the cut |
| **G5 completeness** | all 16 declared individuals present, no substitution | — |
| **G6 determinism** | re-running the full study reproduces every member for every individual exactly | — |

**This gate set is frozen.** No threshold may be moved after results are seen. If a gate fails, the study
is recorded as failed and a successor protocol is written; the existing result directory is never re-run.
The family rule's two clauses (G1 + G2) are exactly as the handoff specified: all three must show median
Δ > 0 and impaired ≥ 0.75, and at least 2 of 3 must be significant at p ≤ 0.01.

## 4. The AC40 four-check, run before this protocol

The four-check framework (`ac40_criterion.py`) was applied to the family at the engineering seeds 0–7
(disjoint from the finals 16–23), **before this protocol was written**:

| member | resolvable | median Δ (own units) | impaired | headroom |
| --- | :---: | ---: | :---: | --- |
| `W_birth` | yes (p 0.0001, n 16) | 208.5 | 87.5% | no ceiling, live sd 4.5 |
| `converted` | yes (p 0.0003, n 16) | 543.0 | 87.5% | no ceiling, live sd 15.0 |
| `memory_writes` | yes (p 0.0005, n 16) | 1389.5 | 87.5% | no ceiling, live sd 102.5 |

Three of the four checks are satisfied on every member. The fourth — stability as a mean/sd ratio — is
**known to not discriminate**: AC40's own finding #2 showed the ratio flags both passing studies and the
failing one (spreads 1.55–7.03) at these sample sizes. Following AC40's guidance, the protocol reports the
impaired fraction and per-individual differences directly (G1, G3) rather than gating on the ratio. The
effect-size requirements are stated in each endpoint's **own units** (the medians above), which is the
error AC41 made and AC40 forbids.

## 5. Predictions registered in advance

1. **Every family member shows median Δ > 0 and impaired ≥ 0.75** on the fresh seeds 16–23 (G1).
2. **At least 2 of 3 members resolve at p ≤ 0.01** — all three did on AC43's final seeds
   (0.000105 / 0.000630 / 0.000290), but the family rule tolerates one member degrading, which is its
   point.
3. **The response remains heterogeneous** — 0 < impaired < 1 for every member (G3). This is AC39's
   bimodality prediction, relocated by AC42 to metabolism and confirmed by AC43 on seeds that played no
   part in locating it; AC45 re-tests it on a third, disjoint seed family.
4. **The protected variant sits above the cut** for every member (G4).

## 6. What is excluded from the claim, in advance

- Not an experience, an understanding, or a life; the endpoints count births, conversions and writes.
- Not autopoiesis or closure; the endpoints are metabolic and maintenance counts, and **AC14 remains a
  negative result** (the zero-nominal-write loop is structurally present and arithmetically inert).
- Not survival; AC34 established the binary alive/dead endpoint is horizon-unstable.
- Not a claim that the capability helps *every* individual: the family rule is an aggregate with stated
  heterogeneity, and no gate tests per-individual dominance.
- Not a general law of development: it is a measured difference between one action set and one
  degradation of it, on a frozen world, at declared seeds.
- Comparisons to anything outside this line are not offered.

## 7. Verification to be performed after the finals

- `audit_ac45.py`: recompute every gate from `rows.jsonl`, independently of the runner.
- `replay_ac45.py`: reproduce two individuals in a fresh process.
- `test_ac45.py`: assert the recorded gate values, the frozen shas, and that the protocol's declared
  source list equals the hashed set (`preflight`).

SOURCES (declared): ac45_family.py ac19.py ac38_variance.py AC45_PROTOCOL_v1.md
