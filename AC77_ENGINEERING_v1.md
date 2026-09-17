# AC77 engineering v1: a long-lived organism does not accumulate environmental signal — the plateau is below a fixed-point noise floor it cannot reduce

2026-09-17. `ac77_engineering.py`, `ac77_engineering_addendum.py`. **No protocol, no final seeds, no
claim.** Prerequisite measurement for content self-production (`ao-content-self-production`): before
building any "better learner", measure whether the signal exists to learn from.

## The question

AC73 established that self-directed rule production is information-limited, not local-optimum-limited:
on single-life scoring a population caps at the same ~0.85 sites below the ceiling as AC30's
single-climber; only oracle (12-seed) scoring reaches the ceiling. The stated cause: the ceiling order
`(2,0,1,3,5,4)` and a mediocre order `(0,1,2,3,4,5)` differ by only ~0.25 sites on the oracle scale while
single-life noise is sd 0.94 — the fine plateau is below the single-life noise floor.

The open question: does a **long-lived** organism accumulate enough *independent* environmental signal
within one lifetime to resolve the plateau? If the noise floor falls as 1/√(independent samples) and a
long life supplies many samples, the plateau is resolvable; if the signal does not accumulate, it is not.

## What was measured

In the AC32/33 regime-B world, over 400 disjoint seeds (8400–8799), the ceiling and mediocre orders were
run to 16,000 ticks, recording (a) the **snapshot** score (sites retained at tick 800, AC30's score) and
(b) the **stationary mean** (time-average of live sites over ticks 8000–16000, the accumulating signal a
long-lived organism actually observes). Then a 42-order stationary-quality survey (100 seeds each)
characterized the ranking's shape.

Anchor first: the AC73 numbers reproduce. Ceiling snapshot@800 sd 0.94; oracle ceiling 12.67, mediocre
12.42, gap 0.250. So this is the same world and the same measurement.

## Result 1: the production signal is a fixed point, not an accumulating series

The decisive structural fact — the live-site count converges to a **seed-specific constant integer**:

| seed | count at t=8000 | count at t=16000 | lost | renewed |
| --- | ---: | ---: | ---: | ---: |
| 0 | 13 | 13 | 11 → 11 | 2652 → 3929 |
| 1 | 11 | 11 | 13 → 13 | 2320 → 3466 |
| 2 | 12 | 12 | 12 → 12 | 2349 → 3471 |

After ~8000 ticks the count is **exactly constant** for every seed (`fixed_fraction = 100%`), no further
site is ever lost, while renewals continue and material accumulates. This is a dynamic fixed point: the
organism's renewal keeps every stressed site alive, so nothing dies, and the count is pinned at whatever
integer survived the early transient (11, 12 or 13). The fixed point is set by the *early* history, not
by anything the organism does later.

Consequence, measured directly (effective-independent-sample analysis, 40 traced lives): the
time-average's noise **does not fall with horizon** — it *rises* from 0.64 (T=800) to 0.78 (T=131,072),
and the effective number of independent samples is **N_eff ≈ 1 at every horizon**. A life of any length
is exactly one sample of the order's quality in that environment. Living longer re-measures the same
fixed point; there are no independent environmental draws to accumulate. The within-life signal is fully
persistent.

## Result 2: the fine plateau is below the fixed-point noise floor — and the 0.25 "gap" is an oracle artifact

The irreducible noise is the across-seed spread of the fixed points: sd **0.83** (ceiling), 0.84
(mediocre), 0.87 (worst). Against that floor, the fine ceiling-vs-mediocre difference is noise:

| measure | ceiling − mediocre (mean ± se, n=400) | AC73's oracle claimed |
| --- | --- | ---: |
| snapshot @ 800 | **+0.075** ± 0.058 | +0.25 |
| stationary mean | **+0.084** ± 0.054 | +0.25 |

The 0.25 oracle gap does **not** replicate over 400 seeds — it collapses to ~0.08, and 0.25 is ~3.4 se
above that. The oracle's 0.25 was a 12-seed sampling fluke: with snapshot sd 0.94 and 12 seeds, the
oracle's own se is ~0.27, so a 0.25 "gap" is within its own noise. The ceiling order and the mediocre
order are **tied** in stationary value; the "fine plateau" AC73 asked about is not a stationary fact.

## Result 3: the stationary ranking is real but shallow at the top

The 42-order survey shows the world *does* rank orders — just not finely:

| | value |
| --- | ---: |
| ceiling `(2,0,1,3,5,4)` | **12.05** (highest; 0 orders above) |
| AC30-best `(3,4,1,5,0,2)` (bad in regime B) | 10.84 |
| min / median / max | 10.47 / 10.98 / 12.05 |
| sd across orders | 0.47 |
| orders within 0.25 of ceiling | **6 / 42** |

The total spread is ~1.6 sites (12.05 to 10.47), but the top of the ranking is a graded plateau whose
adjacent differences are 0.05–0.1 sites — below the single-environment fixed-point noise (0.83), and only
6 of 42 orders are within 0.25 of the ceiling. The **coarse** structure (good ~12 vs bad ~10.5, a ~1.5-site
gap) is real and above the noise floor; the **fine** structure is not.

## The answer, and its reframing

**No — a long-lived organism does not accumulate enough independent environmental signal to resolve the
plateau, for a measured reason: the environment does not supply independent signal within a life.** The
production signal is a fixed point (N_eff ≈ 1), so a life of any length is one sample with sd ≈ 0.83, and
the fine plateau (~0.05–0.25) sits below that floor with no accumulation to reduce it. The only way to
average is across *many* environments — the 12-seed oracle — which is external multi-environment
evaluation, not something a single organism's own single life can do.

Two further facts tighten the answer:

1. The fine plateau is not merely unresolvable — **it is largely not there**. The 0.25 ceiling-to-mediocre
   gap is a 12-seed oracle artifact; over 400 seeds it is +0.08 ± 0.05. Adjacent top orders differ by
   0.05–0.1 sites. There is no 0.25-site ranking to resolve, only oracle noise at that scale.
2. What *is* there, and *is* above the floor, is the **coarse** ranking (~1.5 sites). A self-directed
   learner can reach the good-order plateau (the "63% of margin" AC73 measured = avoid the ~10.5 tail,
   land in the ~12 cluster), but not the optimal order within it.

**For content self-production:** the engineering target must be reframed. A "better learner" built to
resolve the fine plateau is building against a wall that is both a fixed-point noise floor (no within-life
accumulation) and a non-existent stationary difference (the fine ranking is oracle noise). The achievable
self-directed goal is to produce a **good** rule — one in the coarse plateau — from the organism's own
single-life signal, not to recover the optimal rule. That is the claim the content self-production study
should be shaped around (a separation-of-coarse-minima gate, not a fine-margin or ceiling gate).

## Bounds

Engineering prerequisite. No protocol, no final seeds, nothing frozen, nothing claimed about
autopoiesis/consciousness/life. Measured quantities: live-site count (snapshot and stationary mean) in the
declared AC32/33 regime-B ranking world, over disjoint engineering seeds 8400–8799 and 8500–8599. The
"organism observes its own running production and averages it" reading is the least-loaded assumption;
if even that ideal accumulation cannot resolve the plateau, no self-directed mechanism can.

## Artifacts

`ac77_engineering.py` (anchor + fixed-point + gap + noise-floor measurement), `ac77_engineering_addendum.py`
(turnover characterization + 42-order stationary-quality survey). Related: `AC73_ENGINEERING_v1.md` (the
signal-floor measurement this corrects), `AC30_ACQUIRE_v1.md`, `AC32_RESULTS_v1.md`/`AC33_RESULTS_v1.md`
(the oracle and the 12-seed comparator), `DEPENDENCY_AUDIT_v1.md` §3 (the oracle labelled external).
