# AC108 results v1 — cognitive-organizational coupling: both directions confirmed with selective interventions (K7)

2026-09-22. Frozen confirmatory run of the K7 coupling design (`ac108.py`, engineering seeds 0-7,
`AC108_PROTOCOL_v1.md`) on the untouched final family **6100-6107** (8 seeds x 2 histories = 16
individuals), 288 rows. The protocol was hashed in `pre_run_snapshot.json` before any final seed ran.
Audit (`audit_ac108.py`) re-derives the gates, source hashes, coverage and seed-disjointness from the
saved table without simulating; replay (`replay_ac108.py`) reproduces 18 sampled rows and the
determinism re-run exactly. All seven gates pass.

Verdict: **both coupling directions are confirmed, each by a selective intervention with matched
comparisons.** Direction 1 (organizational maintenance -> representational accuracy and use) is
load-bearing: cutting the representation's paid maintenance write leaves it inaccurate 16/16 and
mis-used. Direction 2 (representational function -> adaptation / production / viability) is causal:
forcing the representation's content to the wrong cause reverses the adaptation and collapses
production, 16/16 in the move direction.

---

## 1. The two directions, answered separately

### Direction 1 — maintenance -> accuracy and use: CONFIRMED

The estimate's acquired value is E_world (1); the cut's correct value is E_machinery (0), so the paid
W-gated write (1->0) is what establishes accuracy in the cut. Cutting that write (`no_write`) and
leaving the read honest:

- **Accuracy (robust, 16/16):** `no_write` reads E_world at the cut end in 16/16 (inaccurate); the
  candidate reads E_machinery in 16/16 (accurate). `no_write` writes 0 replicas, 0 attempts — the
  intervention actually cut the maintenance, not the read.
- **Use (behavioural, non-vacuous):** `no_write` relinquishes the still-valid route in the cut on
  seeds 6100, 6101, 6104, 6105, where the candidate holds (0 relinquishments). The inaccurate read
  drives the wrong consumption (relinquish a valid route).
- **Viability (reported, NOT load-bearing here):** `no_write` survives the cut 16/16 (the relinquished
  route is still valid and a blind re-bind re-acquires it), so the use consequence is behavioural, not
  survival-level — exactly the K6 cut pattern (the survival bite is priority-specific and no final seed
  carries the corner priority).

The maintenance is causally load-bearing for representational **accuracy** (16/16) and for **use**
(behavioural, 4/8 seeds); it is not load-bearing for **survival** in this world (disclosed, K6's
boundary).

### Direction 2 — content -> adaptation / production / viability: CONFIRMED

- **Adaptation, move side (robust, 16/16):** the correct content is E_world (relinquish the stale route
  and re-acquire). Forcing E_machinery (`force_machinery`) reverses the adaptation: it holds the stale
  route (0 relinquishments) in 16/16, where the candidate relinquishes >=1 in 16/16.
- **Adaptation, cut side (behavioural, non-vacuous):** the correct content is E_machinery (hold the
  valid route). Forcing E_world (`scramble`) makes the organism relinquish a valid route on seeds 6101,
  6103, 6104, 6105, where the candidate holds.
- **Production / viability (move):** `force_machinery` holds the stale route and **dies 16/16** (the
  material income collapses, W/C die, energy drains); the candidate re-acquires and survives 12/16. The
  content causally determines the production/viability outcome through the adaptation it selects.
- **Production (no-cause):** forcing E_machinery activates the proactive-renewal consumption even
  absent a cause, spending 134-497 extra replicas with identical survival/routes/relinquishments — the
  forced content's disclosed footprint (G5).

The representation's content is causally load-bearing for **adaptation** (both directions) and for
**production/viability** (move side, 16/16); the cut-side content effect is behavioural (K6's boundary).

---

## 2. Integration decision (deliverable 1)

The K6 mechanism already runs on the K3-assessed autonomy baseline's machinery: `ac95.maintain`
(succession, reconstruction, description/pointer/ctrl repair) and the W-gated paid writes are inherited
UNCHANGED by `ac107.py`, and `ac108.py` reuses them through `ac107`'s own factory (G6 re-verifies
byte-identity). The AC105-specific features absent from this world — the corruption challenge and the
allowance-42/persistent-trigger decision-spending refinements — are orthogonal to the
maintenance<->representation coupling and would confound the two-cause discrimination (a corruption
event at the same tick as the cut/move is a THIRD cause). The existing configuration therefore suffices
to answer the coupling question.

Residual, stated not hidden: this is scoped to the AC100-derived, corrupt=False world (BASELINE_v2 §3's
AC106 limitation, inherited by AC107 and here). Whether the cause-estimate's discrimination survives the
AC105 corruption+move grid is a SEPARATE open question, not required for coupling, and is handed to K9.

## 3. Gates (all seven pass, prespecified in the protocol)

| gate | result |
| --- | --- |
| G1 maintenance -> accuracy | **PASS** (no_write wrong 16/16 vs candidate right 16/16; write actually cut) |
| G2 maintenance -> use | **PASS** (no_write relinquishes on 6100/6101/6104/6105 where candidate holds) |
| G3 content -> adaptation (move) | **PASS** (candidate relinquishes 16/16; force_machinery holds 16/16) |
| G4 content causal (cut) | **PASS** (scramble relinquishes on 6101/6103/6104/6105 where candidate holds) |
| G5 clean control | **PASS** (no_write/scramble byte-identical to candidate in no_cause; force_machinery adds only proactive spend) |
| G6 frozen-copy reproduction | **PASS** (candidate/r2/r4/scramble reproduce ac107 byte-for-byte) |
| G7 completeness/determinism | **PASS** (288 rows; determinism re-run) |

## 4. Survival (reported, NOT gated — bimodality-aware lower bounds)

| arm | cut | move |
| --- | --- | --- |
| candidate | 16/16 | 12/16 (dies 6100, 6107) |
| no_write | 16/16 | — |
| scramble | 16/16 | — |
| force_machinery | — | **0/16** (dies all) |
| r2 | 16/16 | — |
| r4 | — | 6/16 (dies 6100, 6102, 6103, 6104, 6107) |

Priorities of 6100-6107: `[1,2,3,0] [3,1,2,0] [1,0,2,3] [2,3,0,1] [1,2,3,0] [1,3,0,2] [1,2,0,3]
[0,1,3,2]`. None is the priority-corner `[3,0,2,1]`, which is why the cut's survival bite does not recur
on this family (K6's vacuous cut, reproduced) while the *behavioural* relinquish contrast does.

## 5. Causal dependence vs superior performance (distinguished)

- **Causal dependence (gated, G1-G4):** forcing the content or cutting the maintenance changes the
  per-individual behaviour. This establishes that the representation is *used* and *maintained* — it is
  not a redundant name.
- **Superior performance (reported, not gated):** the candidate (correct per-cause content) beats the
  externally supported rival r4 in the move by 12/16 vs 6/16 (a clean 2x separation), and matches r2 in
  the cut (16/16 both — the cut does not bite r2 on this family, so there is no cut-side edge, K6's
  lesson). The candidate's own move deaths (6100, 6107) are the re-acquisition boundary (relinquished,
  failed to re-bind, starved — the AC83/AC74 path), an operating-range limit, not a coupling failure.

## 6. Claim discipline

The strongest wording earned: "**cutting the representation's paid maintenance write leaves it
inaccurate in 16/16 individuals, and forcing its content to the wrong cause reverses the organism's
adaptation and collapses its production/viability (16/16 in the move direction), with each effect
isolated by a single-flag intervention and matched against the maintained candidate and externally
supported fixed-threshold rivals.**"

No survival contrast is gated (K6's lesson); no metacognition, autopoiesis, or "alive" claim. Seeds are
the replication unit (8 independent units, not 16). Engineering seeds 0-7 are excluded from the final
sample.

## 7. Recheck of inherited claims (K6)

- The frozen arms reproduce AC107 byte-for-byte (G6), so K6's discrimination (Q1) and storage-maintenance
  (Q3) claims are unaffected by the extension.
- K6's negative (Q2/Q4 survival seed-boundedness) is confirmed, not overturned: the cut's death bite is
  still priority-specific (r2/scramble/no_write survive the cut 16/16 on this family).
- The move-side advantage (candidate vs r4) is present and now cleaner than K6's (12/16 vs 6/16 here,
  against K6's 14/16 vs 10/16), on a fresh family.

## 8. What this hands downstream

- **K9 (synthesis):** the cognitive-organizational coupling is now established in BOTH directions, each
  by a selective intervention with matched comparisons — the first time the level-(c) representation has
  been shown causally coupled to the level-(a/b) maintenance machinery, not merely co-present. The two
  directions are: maintenance sustains representation (accuracy robustly, use behaviourally), and
  representation drives adaptation and viability (move side robustly, cut side behaviourally).
- The residual for a future card: the cause-estimate's discrimination under the AC105 corruption+move
  grid (the integration this study scoped out), and the re-acquisition boundary (candidate move deaths
  6100/6107) — both operating-range questions, not coupling gaps.
