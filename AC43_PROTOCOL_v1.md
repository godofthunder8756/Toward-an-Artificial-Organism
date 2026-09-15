# AC43 PROTOCOL v1 — registered before the first final seed

**Endorsement.** This protocol was written and its source list hashed **before** any final seed was run.
The result directory is created with `mkdir(exist_ok=False)`, so a frozen directory can never be
overwritten. A self-declared defect elsewhere causes a hash mismatch; none is declared here.

## 1. The claim, in the form its own shape permits

*An organism whose register occupancy is maintained by the repair action produces more W births over a run
than one whose occupancy is not, under corruption absent.*

The endpoint is **`ledger.W_birth`** — selected by AC42's survey of all 15 scalar quantities the AC19
machinery exposes, as a quantity with variance, headroom, and a resolved live-vs-cut contrast, and as a
metabolic rather than a per-tick measure. `ledger.active` (AC39's endpoint) and
`register_replicas_set_total` (AC41's endpoint) were rejected by that survey for zero headroom and zero
variance respectively, and neither may be substituted here.

**The claim is an aggregate with stated heterogeneity, and the gate is written that way.** AC42 measured
that the cut arm's response is bimodal: 88% of individuals impaired, 12% not. A separation-of-minima gate
("capable worst ≥ bar AND cut best < bar") would therefore fail by construction, and declaring one would
repeat AC17's design error. The claim does not assert that the capability helps *every* individual, and no
gate here tests that it does.

## 2. Design

| item | declared value |
| --- | --- |
| capable arm | `two_way` |
| cut arm | `two_way_no_repair` |
| second capable variant | `two_way_protected` (gate G5 only) |
| **corruption** | **absent** — `reg_rate = 0.0`, so AC14's integrity channel is off by construction |
| endpoint | `ledger.W_birth` (W births over the run) |
| individuals | **seeds 8–15 × histories (0, 1) = 16** |
| freshness | engineering in AC41/AC42 used seeds 0–7 only; these 16 individuals are disjoint from it |
| runner | `ac43_capability.py` (`main`), result directory `ac43_results_v1/` |
| sources | hashed into `pre_run_snapshot.json` before the first individual |

## 3. Declared gates — all seven must pass

| gate | criterion | declared from |
| --- | --- | --- |
| **G1 resolvability** | exact sign-flip test on the 16 paired differences, **p ≤ 0.01**, and n ≥ 8 (power floor 2/2ⁿ = 0.00003 at n = 16) | AC38's lesson: resolvability is tested, not assumed |
| **G2 effect size in endpoint units** | **median paired difference ≥ 150 births** | AC42 measured 208; the bar sits under it with margin, *in this endpoint's own units* — the error AC41 made was copying a requirement from another ledger |
| **G3 impaired fraction** | **≥ 0.75** | AC42 measured 0.88 |
| **G4 heterogeneity present** | 0 < impaired fraction < 1 | the bimodality is part of the claim, so a claim of uniformity is not permitted to pass |
| **G5 protected variant** | median(`protected` − `cut`) > 0 | a second, independently-degraded capable arm must sit above the cut |
| **G6 completeness** | all 16 declared individuals present, no substitution | — |
| **G7 determinism** | re-running two individuals reproduces their W_birth exactly | — |

**This gate set is frozen.** No threshold may be moved after results are seen. If a gate fails, the study
is recorded as failed and a successor protocol is written; the existing result directory is never
re-run. That rule was earned by AC16, where a margin gate was the wrong *shape* and the attempt to
re-choose the threshold was refused in the project's own instructions.

## 4. Predictions registered in advance

1. **The metabolic response is bimodal** (~88% impaired). AC39 predicted a bimodality for the *activity*
   endpoint and AC41 falsified it for *occupancy*; AC42 located it in the **metabolic** family. If the
   final seeds show no heterogeneity (G4 fails), the prediction is falsified on fresh data.
2. **Median difference ≈ 208**, from AC42's engineering, at a comparable live-to-cut ratio.
3. **No individual is expected to be *hurt* by the capability** (differences ≥ 0), consistent with AC42.

## 5. What is excluded from the claim, in advance

- Not an experience, an understanding, or a life; `W_birth` counts W-region births over a run.
- Not autopoiesis or closure; the endpoint is a metabolic count, and **AC14 remains a negative result**
  (the zero-nominal-write loop is structurally present and arithmetically inert).
- Not survival; AC34 established that the binary alive/dead endpoint is horizon-unstable.
- Not a general law of development: it is a measured difference between one action set and one
  degradation of it, on a frozen world, at declared seeds.
- Comparisons to anything outside this line are not offered.

## 6. Verification to be performed after the finals

- `audit_ac43.py`: recompute every gate from `rows.jsonl`, independently of the runner.
- `replay_ac43.py`: reproduce two individuals in a fresh process.
- `test_ac43.py`: assert the recorded gate values, the frozen shas, and that the protocol's declared
  source list equals the hashed set (`preflight`).

SOURCES (declared): ac43_capability.py ac19.py ac38_variance.py AC43_PROTOCOL_v1.md
