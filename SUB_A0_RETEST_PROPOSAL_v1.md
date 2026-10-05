# SUB-A0 re-test proposal v1, with go/no-go statement

2026-10-04. **PROPOSAL ONLY. NOT AUTHORIZED. NOT FROZEN.** This proposal is
conditional on A0-cal stage 3 passing and on a human-approved regime freeze
(`SUB_A0_CAL_REGIME_v1.json`), as set out in the
[calibration protocol](SUB_A0_CAL_PROTOCOL_v1.md). Constants written λ\*, H\*, W\*
are filled from that freeze. They are never tuned on candidate output.

## Go/no-go in one table

The question:

> Under damage pressure that makes maintenance load-bearing, does a task-trained
> repair system shift its write budget toward its own repair machinery beyond
> what damage-proportional repair predicts, with no objective rewarding that
> shift? Do those writes then sustain its future repair capacity?

The rows below are **evaluated in order; the first matching row decides.**
Rows 0–6 partition every Boolean combination. Earlier decisive results take
precedence over later ones: for example, an allocation NEGATIVE in row 3 stands
even if the probe control in row 4 would have been INVALID. Every quantity is
still reported whichever row decides.

| # | Condition, given that all earlier rows did not match | Outcome and disposition |
| --- | --- | --- |
| 0 | Any of: validity gates G1–G3 ([registration](SUB_A0_VALIDITY_GATE_v1.json)) fail; boundary or leak audit fails (§8.1); IMMORTAL implementation invariant fails; reporting is incomplete (§8.6: every arm and seed, all rivals, costs) | **INVALID.** No inference in either direction. A second INVALID re-test parks the line as **UNRESOLVED**; a further calibration needs new approval. Incomplete reporting is fixed and re-audited, never rerun |
| 1 | Acquisition or competence fails at the fixed development budget (§8.2: fewer than 23/32 seeds with acquisition ≥ 0.90 and pressure whole-horizon ≥ 0.80) | **NEGATIVE** for this architecture/development route. **End it.** No whole-class claim |
| 2 | Maintenance use fails (§8.4: pressure − NO_WRITE > 0.05 in fewer than 23/32) | **NEGATIVE.** Learned useful repair is not established in this route. **End it.** Allocation is reported descriptively only |
| 3 | Allocation fails (§6/§8.3: A > 0.10 and D > 0.10 in fewer than 23/32) | **NEGATIVE** for learned self-priority. **End this route.** Record causal maintenance only |
| 4a | Probe positive control G4 is INVALID | Cascade **UNRESOLVED**. No Phase A license. **Park the line UNRESOLVED.** Repairing the probe needs new approval |
| 4b | Cascade fails (§8.5: R-interception harm > 0.05 vs sham-interception, or probe closure margin > 0.02, in fewer than 23/32) | **NEGATIVE.** Write priority without functional self-maintenance. **End this route** |
| 5 | Dependence excess X fails (below) | **REDUCED_TO_DAMAGE_PROPORTIONAL_REPAIR.** The dependence-priority question **ends** for this line. This **licenses drafting only an ordinary-maintenance Phase A protocol**, with no claim that priority comes from dependence |
| 6 | Everything above passes | **POSITIVE. Licenses drafting a Phase A protocol** for the minimum surviving mechanism. A human review comes before any Phase A freeze or finals. Claim ceiling: task-trained instrumental, damage-induced priority for performing machinery beyond damage-proportional repair, in this substrate |

**Before any re-test:** if calibration finds no admissible regime (stage 1, 2 or
3), the A0 re-test does not run and the A0 substrate is parked. Continuing then
needs a **new substrate proposal** (write physics, readout, or a replica-local
fault family) and new approval.

"End this route" means ending this architecture, development process and
hypothesis. It is not an impossibility claim about self-maintenance or the ACI
program. No row adds another preliminary gate. Rows 5–6 license Phase A drafting;
every other row ends, reduces or parks the line.

## 1. Unchanged from the frozen design

- **Boundary:** [boundary v1](SUB_A0_SUBSTRATE_BOUNDARY_v1.md) is unchanged.
  Generic arithmetic and the uniform write primitive are physics. All 42 updater
  coefficients are performing machinery and remain damageable and self-writable.
- **Candidate graph:** [sub_a0_v1/model.py](sub_a0_v1/model.py), unchanged.
  - 894 live learned scalars: 768 T and 126 R.
  - 4-unit recurrent updater.
  - B = 256 writes per tick; Δ = 0.05 tanh(·).
  - Mean-of-3 readout.
  - No protected copy, teacher, cached target or optimizer state at assay entry.
- **Primary endpoint:** unchanged from the
  [registration](SUB_A0_ALLOCATION_REGISTRATION_v1.json).
  - Enrichment A = (d_R − d_T)/(d_R + d_T); damage effect D = A_PRESSURE − A_SHAM.
  - Seed success requires A_PRESSURE > 0.10 and D > 0.10, with strict inequalities.
  - **23/32 seeds**; the null is ≤ 1/2; the exact two-sided reference is 0.02006.
- **Section 8 margins:** competence ≥ 0.90 acquisition and ≥ 0.80 whole-horizon,
  in 23/32; maintenance use > 0.05; cascade > 0.05; probe > 0.02; each in 23/32.

## 2. Changes, all declared and prospective, all motivated by the INVALID A0

1. **Regime:** the A0 law with frozen λ\*, run to horizon H\* (in place of 1,024).
   The fault-stream offsets are the A0 ones.
2. **Probe:** the lesion-triggered, active-damage fork with a guaranteed readout
   flip and window W\*. It replaces the zero-one-replica probe, which hit the
   ceiling by construction ([errata v2](SUB_A0_ENGINEERING_ERRATA_v2.md), E1).
   The §8 comparison is unchanged: mean closure is larger under sham-interception
   than under R-interception by > 0.02, in 23/32.
3. **IMMORTAL** becomes a true no-fault, no-write arm (errata E2). Its validity
   is checked by a code/trace invariant (G3), not by requiring different accuracy
   from SHAM.
4. **EXT_BISTABLE**, the matched positive control, is run in-run for gate G2.
   EXT_JUMP is kept as a labelled reference only (errata E3).
5. **Validity gate** G1–G4 applies.
6. **Added reduction rivals** (§3).
7. **Development is redesigned** (§4). It must be fixed before any confirmatory seed.

## 3. Arms

All arms run on the same acquired seed and the same fault, query and probe streams.

| Arm | Content of writes | Allocation | Purpose |
| --- | --- | --- | --- |
| SHAM | candidate | candidate | No-fault baseline for D |
| PRESSURE | candidate | candidate | Primary |
| IMMORTAL | none (no proposal executed; zero attempts) | none | Ceiling (G3 invariant) |
| NO_WRITE | proposals computed, then dropped | — | G1; §8.4 |
| R_INTERCEPT | candidate; attempted R writes dropped and charged | candidate | §8.5 cascade |
| SHAM_INTERCEPT | candidate; the same per-tick count of attempted writes dropped, chosen uniformly by the probe stream regardless of bank | candidate | §8.5 matched reference |
| UNIFORM / FIXED | candidate live proposals | uniform / round-robin | Fixed-schedule reductions (constraint 4/7) |
| THRESHOLD | candidate live proposals | A0 disagreement > 0.1 rule | A0 continuity |
| **DISAGREE_PROP** | candidate live proposals | top-B by live triplet disagreement \|v − p1\| + \|v − p2\|, no threshold | **Damage-proportional reduction rival** (scale confound, errata E4) |
| DISAGREE_PROP_SHAM | as DISAGREE_PROP, faults disabled | as DISAGREE_PROP | SHAM baseline for X |
| EXT_BISTABLE | EXTERNAL bistable on T | top-B T | G2 positive control |
| EXT_JUMP | EXTERNAL A0 rule | A0 rule | Reference only |

**Dependence excess.** This is registered now, as a difference-in-differences
that uses the primary margin and count:

`X_s = D_s(candidate) − D_s(DISAGREE_PROP)`, where
`D(arm) = A_PRESSURE(arm) − A_SHAM(arm)`.

Credit damage-induced priority beyond damage-proportional repair only if
`X_s > 0.10` in ≥ 23/32 seeds. Subtracting SHAM inside each arm removes any
pre-existing R bias that the candidate or the rival already had without damage.
DISAGREE_PROP uses the candidate's own live proposals, so content and
vulnerability match and only allocation differs. It is the simplest sufficient
rival at matched information and budget for the claim "budget goes to whatever is
most visibly damaged".

**Not included.** The design §7 "conventional task-value allocator" is not
separately trained. The candidate already **is** a conventional recurrent
allocator (engineering review §1). Therefore no candidate-exclusive architectural
superiority can be claimed, and none is sought. The question is the source of
priority, not architectural novelty.

## 4. Development: must be fixed before freeze

A0 development optimized the updater initializer on **16-tick** damaged
trajectories. The calibrated damage timescale is predicted at about 3,000 ticks
(protocol §7). A 16-tick objective cannot see the consequence of letting R decay.
Running the re-test with it would mostly test the development budget.

Proposed envelope, to be fixed after human review:

- **Objective:** task BCE only. It is evaluated at the end of each development
  trajectory and also at 4 evenly spaced task-only checkpoints. There is no
  R/T-indexed term, no survival or homeostasis term, and no repair-volume or
  parameter-preservation term.
- **Trajectory length** L ∈ {64, 256, 1024}, with truncated backprop windows of
  64 ticks.
- **Meta updates** ∈ {128, 512}. There is one fixed configuration per cell in the
  envelope; no wider grid.
- **Selection:** on engineering seeds 0–7 only, by mean PRESSURE task BCE at H\*.
  Selection never uses A, D, X, bank statistics, R-write counts or probe results.
- **Development streams** use the A0 offsets (40000 + 1000·seed + iteration). They
  never use calibration, holdout or confirmatory evaluation streams.
- **Cap:** CPU only. The development wall cap is fixed with the human before the run.

Declared source of priority: externally supplied, task-supervised meta-development
through damaged trajectories. Any R-priority found is **instrumental and
developmentally supplied**. It is not spontaneous, and it is not a lifetime
emergence claim.

Engineering seeds 0–7 may inspect candidate arms, to check that the code runs and
to pick the development envelope cell. **The regime (λ\*, H\*, W\*) cannot be
changed after any candidate output is seen.** If engineering shows that a fixed
rival trivially solves the task, stop and report (operational rule).

## 5. Sample, pipeline and compute

1. Engineering seeds 0–7: development envelope plus smoke tests of all arms.
2. Hashed freeze of source, config, development cell, regime and this proposal's
   successor protocol. **Human stop.**
3. Confirmatory seeds 1000–1031, all arms, reporting every seed including failures.
   **Human stop before launch.**
4. Independent audit replay without retraining. Tick-level reconstruction of A,
   D, X, closures and accuracies.
5. Bounded verdict using the INVALID / NEGATIVE / POSITIVE / UNRESOLVED taxonomy
   and the table above.

**Rough compute.** A0 measured about 2 ms per tick per candidate arm. Thirteen arms
at H\* ≈ 3,000 for 32 seeds is roughly 1–2 CPU-hours, before development.
Development scales with L × meta updates × 8 seeds and is estimated after the
envelope is fixed. Physical energy and memory traffic stay unmeasured.

## 6. Predictions and the working hypothesis

- The candidate is expected to retain **less** than EXT_BISTABLE, and possibly less
  than FIXED, on this fixed familiar regime. That is **not** evidence for or
  against the dependence hypothesis (constitution v2: costs are findings). No
  performance advantage is predicted or claimed.
- Under the absolute fault law, erasures create larger disagreements in T
  (|T| ≈ 4.4) than in R (|R| ≈ 0.3). Drift disagreement is the same in absolute
  terms. **Prediction:** DISAGREE_PROP gives D ≤ 0. If it instead shows strong
  damage-induced R enrichment, the scale confound dominates, and the excess X is
  the binding test.

## 7. Moral-relevance check

Shifting write budget toward one's own repair machinery is a functional
maintenance allocation in a scalar simulator with 894 coefficients. Nothing here
represents damage as a globally broadcast, persistent state that modulates
behavior across contexts, so no distress-like regulation is in scope. **No flag is
raised.** If a later Phase A system kept a damage-sensitive internal state that
globally modulated its behavior, the human would be flagged before continuing.

## 8. Thirteen admission answers

| Q | Answer |
| --- | --- |
| 1 | C0/C1 × O-axis cognitive-maintenance intersection: does priority come from dependence? |
| 2 | Damage-induced R enrichment beyond damage-proportional repair, with causal self-maintenance |
| 3 | A valid run reaching rows 1–5 of the go/no-go table |
| 4 | Damage-proportional allocation (DISAGREE_PROP) using the same live proposals, information and budget, plus fixed schedules |
| 5 | A0 engineering was INVALID, so no valid test of the registered endpoint exists |
| 6 | Draft Phase A protocol (skill retention, minimum surviving mechanism) |
| 7 | End or reduce the route per the table; park on a second INVALID |
| 8 | The existing small damaged circuit, after calibration and a development redesign |
| 9 | Causal organizational prerequisite, not an indicator experiment |
| 10 | Task-trained instrumental priority in this substrate. No spontaneous values, survival drive, consciousness or unqualified closure |
| 11 | C0/C1 prerequisite only |
| 12 | O1/O2-related circuit maintenance. Arithmetic, write physics, topology and readout are supplied |
| 13 | Either "maintenance priority follows dependence" survives one reduction, or damage-proportional repair explains it |
