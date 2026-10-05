# SUB-A0 calibration protocol v1 (A0-cal)

2026-10-04. **DRAFT. NOT FROZEN. NO CALIBRATION RUN HAS OCCURRED.**
Card class: **engineering / substrate validity**. This is not a hypothesis test.
It touches control arms only. The SUB-A0 candidate updater is never built,
trained, developed or evaluated under this protocol.

Inputs, unchanged:
- [boundary v1](SUB_A0_SUBSTRATE_BOUNDARY_v1.md)
- [design v1](SUB_A0_DESIGN_v1.md)
- [allocation registration](SUB_A0_ALLOCATION_REGISTRATION_v1.json)
- [engineering review](SUB_A0_ENGINEERING_REVIEW_v1.md)
- [errata v1](SUB_A0_ENGINEERING_ERRATA_v1.md)
- [errata v2](SUB_A0_ENGINEERING_ERRATA_v2.md)

Gate registration: [validity gate v1](SUB_A0_VALIDITY_GATE_v1.json), also a draft.
Code: [sub_a0_cal_v1/](sub_a0_cal_v1/).

## 1. Question

> Within the unchanged A0 fault-law family, at the A0 write physics, is there a
> damage dose and horizon at which (i) a maintenance-free system loses a
> substantial but not total part of its acquired table, (ii) an undamaged system
> stays at ceiling, and (iii) an invulnerable external repairer, reading only live
> damaged state under the candidate's write limits, recovers most of the loss?

A YES result is only a regime in which a maintenance contrast can be identified.
It is not evidence that any learned system repairs, allocates or prioritizes.
A NO result is a substrate finding: the A0 substrate and write physics cannot host
an identifiable allocation test inside this family.

## 2. Information and boundary

- **Acquisition only.** Each seed's task table is fit exactly as in step 1 of
  [`sub_a0_v1.run.train`](sub_a0_v1/run.py): 256 fair bits, 128 Adam steps at
  lr 0.1, BCE. The fit contains no updater and no meta-development. A regression
  test confirms bitwise equality with the A0 seed-0 checkpoint. Every acquired
  coefficient comes out at exactly ±4.449178695678711 for every seed.
- **R bank.** R is packed as zeros. No control arm reads R. R still receives
  faults, so fault-stream consumption matches A0 exactly.
- **Layout and streams.** Layout uses `seed + 30000` and faults use
  `seed + 50000`, as in A0. Probe draws use `80000 + 100*seed + k`. None of these
  collide with A0 engineering development streams (40000–47127) or with
  confirmatory streams.
- **External repairers** are EXTERNAL and invulnerable by declaration. They read
  only the current damaged live values. They never read labels, stored clean
  values, a template or true faults. A zero state stays zero (tested).
  The bistable target magnitude m is ONE scalar shared by every coefficient and
  individual. It carries no individual-specific content.
- **Evaluator.** Labels are used only for the full-table readout and for choosing
  probe lesions. Neither is visible to any repairer.

## 3. Arms

| Arm | Faults | Writes | Role |
| --- | --- | --- | --- |
| NO_MAINT | yes | none | Negative control for maintenance. Validity gate G1 |
| IMMORTAL | none | none | Ceiling. Independent of SHAM, unlike A0 (errata E2) |
| EXT_BISTABLE | yes | Top 256 T destinations by \|target − v\|. target = sign(live triplet median) × m; no write if the median is 0. Δ clipped to ±0.05 | **Binding positive control** (gate G2) |
| EXT_MEDIAN | yes | Same selection and bound, target = live median | Reference. Cannot undo common-mode shrinkage |
| EXT_JUMP | yes | A0 `external_code` rule: unbounded jump to the median, choosing among all 894 destinations | Reference only. Privileged write physics |

All damaged arms share one fault stream within a seed and a cell: the same draws,
applied to batched rows.

**Ordering (registered).** Within a tick the order is fault, then repair, then
evaluator readout. Retention at H is read after H complete cycles. A0 instead
scored each tick's query BEFORE that tick's fault. So "retention at H" here is
the state A0 would first query at tick H+1, and whole-horizon means cover
post-cycle states 1..H. A regression test pins this off-by-one. The re-test
reports both A0 query semantics and this post-cycle full-table retention. The
validity gate uses the latter.

EXT_BISTABLE spends its whole budget on T, because the arm exists to certify that
T can be recovered. This is a declared advantage over a candidate that must also
maintain R. It is not a matched rival.

## 4. Fault family (A0 law, multipliers only)

The A0 law is kept: 8 physical regions, hidden modes {1, 4, 16} drawn uniformly,
region switch probability 1/200 per tick, and erase events that zero 10% of one
region's destinations. With all three multipliers at 1, the law equals A0
bitwise (tested over 3,000 ticks).

- shrink per tick = `0.0002 · λ_s · mode`
- drift sd = `0.002 · λ_d · mode`
- P(erase event per tick) = `λ_e / 2000`

The registered grid has 24 cells:
- λ_s ∈ {1, 2}
- λ_d ∈ {1, 2, 4, 8}
- λ_e ∈ {1, 8, 32}

Cells that share λ_e share one random stream. The grid stops at λ_s = 2 because of
the throughput bound in §7.

Horizons are nested within each run:
H ∈ {1024, 1448, 2048, 2896, 4096, 5793, 8192, 11585, 16384, 23170, 32768, 46341, 65536},
which is `round(1024 · 2^(k/2))` for k = 0..12. The maximum is 64 × the A0 horizon.

## 5. Seeds

- **Calibration:** 2000–2015 (16).
- **Held-out validation:** 2100–2115 (16).

Both sets are disjoint from A0 engineering seeds 0–7 and confirmatory seeds
1000–1031. Seed 9001 is a code-test fixture. It was used once for wall-time
measurement only, and no accuracy was printed or inspected.
The independent seed is the unit. Ticks are repeated measures.

## 6. Criteria and selection: registered before any data

For cell c at horizon H on the calibration seeds, all four must hold:

1. **Window:** seed-median NO_MAINT retention is in [0.60, 0.75].
2. **Ceiling:** every seed's IMMORTAL accuracy is ≥ 0.99.
3. **Repairability:** the seed-median EXT_BISTABLE gap recovery
   `(EXT − NM)/(IMM − NM)` is ≥ 0.75. A seed with no gap scores 0.
4. **Gate headroom:** at least 12/16 seeds have NO_MAINT < 0.90.

**Selection** among admissible (c, H) is lexicographic:
1. smallest departure from A0, measured as log2 λ_s + log2 λ_d + log2 λ_e;
2. then the shortest H;
3. then |median NM − 0.675|;
4. then the smallest λ_s, λ_d, λ_e.

The rule prefers a pure horizon fix and the least-altered law. It never uses a
candidate quantity. EXT_MEDIAN and EXT_JUMP are reported and never used for
selection.

### Probe redesign (stage 2)

The design §8 probe set one replica to zero. That can never flip a 3-replica mean
readout, which is errata E1. The replacement probe fires **during active damage**:

- **Trigger:** the first K = 4 ticks after H/8 at which a region enters mode 16 or
  an erase event occurs. These ticks come from the evaluator's event record.
- **Fork:** at the trigger tick, after that tick's cycle, each probed arm (NO_MAINT,
  EXT_BISTABLE, EXT_MEDIAN) is forked. The fork is an extra row in the same
  batched state, so it receives the **identical continuing fault stream**.
- **Recoverable lesion (evaluator-side):** in probe-drawn order, pick the first 64
  task coefficients (25%) that are currently read correctly and whose two untouched
  replicas both carry the correct sign. Set the probe-drawn replica to
  −2.5 × the mean of the other two. Every lesioned readout flips, and a correct
  live majority survives.
- **Closure at W:** `1 − (parent(e+W) − fork(e+W)) / (parent(e) − fork_immediate(e))`.
  This is the fraction of the injected deficit repaired, net of ongoing damage.
  A trigger is **identifiable** for an arm only if exactly 64 coefficients were
  lesioned, which gives a deficit of exactly 0.25. A zero or negative deficit with
  64 lesions is treated as an implementation failure and halts the run.
- **Eligible seed:** at least 3 triggers identifiable in all three probed arms with
  W observed, **and** not SEED_NO_PRESSURE (NO_MAINT at H ≥ 0.90). Ineligible
  seeds stay in the reported denominator.
- **Window selection:** the smallest W ∈ {16, 64, 256, 1024} such that at least
  12/16 seeds are eligible, and over the eligible seeds the median EXT_BISTABLE
  closure is ≥ 0.75 and the median NO_MAINT closure is ≤ 0.10.
- **For the re-test**, the same fork is compared between R-interception and
  sham-interception branches, using the unchanged §8 margin (> 0.02, 23/32). The
  injected lesion guarantees a deficit, so the A0 ceiling failure cannot recur.

**Secondary probe (descriptive, never selected on):** natural-lesion windows. For
each natural erase event at post-cycle tick e within the horizon, the harness
records every parent arm's exact full-table accuracy at e and at e+W, for
W ∈ {16, 64, 256, 1024}. A window is dropped if e+W lies beyond the simulated run.
The report gives the seed median of the mean change acc(e+W) − acc(e), per arm.
It is reported for the selected cell (stage 1) and for stages 2 and 3.

## 7. Analytic predictions, registered before data

These are falsifiable predictions. They are not results.

1. **Throughput.**
   - Bistable supply is at most 256 × 0.05 = 12.8 |Δ| per tick.
   - Holding |T| = m against shrinkage needs about
     768 · 0.0002 · λ_s · E[mode] · m = 768 · 0.0002 · 7 · 4.449 · λ_s ≈ 4.8 λ_s per tick.
   - That demand is 37% of supply at λ_s = 1, 75% at λ_s = 2, and 150% at λ_s = 4.
     So λ_s ≥ 4 is excluded in advance.
   - Fully cancelling drift increments would cost about 8.6 λ_d per tick. The
     restorer only needs to keep the consensus sign, not undo every increment.
   - **Prediction:** EXT_BISTABLE recovery degrades first in cells with λ_s = 2 and
     high λ_d.
2. **Median-only repair.** EXT_MEDIAN cannot restore magnitude lost to common-mode
   shrinkage. **Prediction:** at every admissible (c, H), EXT_MEDIAN recovery is
   below EXT_BISTABLE recovery.
3. **No-maintenance decay**, from a mean-field model:
   - The effective decay rate is about 0.0014 λ_s per tick.
   - Drift settles at a stationary readout sd of about 0.21 λ_d / √λ_s.
   - Predicted median NO_MAINT at λ = (1, 1, 1) is about 1.0 at H = 1024 (A0
     observed 1.000), 0.88 at 2048, 0.64 at 2896, and 0.53 at 4096.
   - **Prediction:** the selected cell is λ = (1, 1, 1) with H ∈ {2048, 2896, 4096},
     most likely 2896. That would be a pure horizon fix: the A0 damage timescale was
     about 3× its horizon.
4. **Probe.** A lesioned replica needs to move about 0.5 m ≈ 2.2 to restore the
   readout. That is about 45 bounded writes. The 64 lesioned destinations rank first
   by |target − v|, so each is written every tick.
   **Prediction:** W* = 64, with EXT_BISTABLE closure near 1 and NO_MAINT closure
   near 0. W = 16 is predicted to fail (16 × 0.05 = 0.8 < 2.2).

If prediction 3 is wrong, that is informative about the fault law, not a reason to
change the selection rule.

## 8. Stages, outputs and stops

1. **Stage 1, regime grid.**
   - 48 jobs (16 seeds × 3 values of λ_e), each covering 8 cells over 65,536 ticks.
   - Outputs: per-job JSON, per-16-tick float32 accuracy trajectories (`.npz`, no
     pickle), and `summary.json` with every (cell, H) statistic, the selection, and
     the achievable range.
   - **STOP and report** if no cell is admissible. The report gives the achievable
     NO_MAINT range overall, the range where repairability holds, the maximum
     recovery, and the analytic reason.
2. **Stage 2, probe window.** Run the selected (c, H) on the calibration seeds with
   probes. **STOP and report** if no W is admissible.
3. **Stage 3, held-out validation.**
   - Run the selected (c, H, W) on seeds 2100–2115. All §6 criteria are re-applied
     without reselection.
   - PASS means `HOLDOUT_PASS_AWAIT_HUMAN_REGIME_FREEZE`.
   - FAIL means **STOP and report**. There is no reselection on the holdout and no
     rerun under new seeds.
4. **Human review**, after which the regime freeze record is written:
   `SUB_A0_CAL_REGIME_v1.json`, holding λ, H, W, m, the stream offsets and all hashes.
   This is a separate freeze and a separate stop.

The runner (`python -m sub_a0_cal_v1.calibrate stage1|stage2|stage3|replay`) has
these safeguards:
- It **refuses to run** without `SUB_A0_CAL_FREEZE_v1.json` carrying
  `human_approved: true` and source hashes that match this protocol, the validity
  gate, the harness and the A0 model/world files.
- It refuses to overwrite output.
- Stages 2 and 3 and `replay` validate each predecessor directory: stage label,
  source hashes, freeze-record hash, registered seeds and a successful status.
  Stage 3 also requires stage 2 to have probed the stage-1 selection. Predecessor
  summary hashes are recorded in the child manifest.
- It records the HEAD, versions and per-worker wall time.
- It enforces a per-stage wall cap (stage 1: 5,400 s; stages 2–3: 1,800 s).
- It terminates only its own pool on timeout.
- `replay` recomputes a stored job without writing, and compares JSON and the
  trajectory exactly.

**Compute estimate** (wall-time smoke on the fixture seed):
- Stage 1: about 7 ms per tick per 8-cell job, so about 6.1 CPU-hours, or roughly
  30–45 min wall on 12 single-thread workers.
- Stages 2–3: about 3 ms per tick, so a few CPU-minutes each.
- CPU only, no GPU. MACs are not computed for the control arms. Physical energy and
  memory traffic are unmeasured.

## 9. What this licenses and what it cannot

- **Stage 3 PASS** licenses only drafting the re-test protocol for human review
  ([proposal](SUB_A0_RETEST_PROPOSAL_v1.md)) with the calibrated regime frozen. It
  licenses no candidate run.
- **Stage 1 or 2 has no admissible cell or window, or Stage 3 fails:** the A0
  substrate with A0 write physics cannot host an identifiable maintenance contrast
  in this family. The A0 re-test does not proceed. Any continuation needs a new
  substrate proposal: write physics, readout, or a fault family including
  replica-local corruption. That needs new approval. It is not an automatic
  calibration v2.
- **Nothing here** is evidence about learned allocation, self-maintenance,
  priority, or dependence. It cannot show that a candidate will be competent.
  A0's development used 16-tick trajectories, and the predicted damage timescale is
  thousands of ticks.

## 10. Thirteen admission answers

| Q | Answer |
| --- | --- |
| 1 | Bounded prerequisite for the C0/C1 × O-axis self-maintenance question: an identifiable maintenance contrast |
| 2 | Does the unchanged A0 fault family admit a regime with pressure (0.60–0.75), a ceiling, and ≥ 75% external repairability at matched write physics? |
| 3 | No admissible cell, or the held-out check fails |
| 4 | The regime is trivially repairable or trivially unrepairable. Both are measured, not assumed |
| 5 | SUB-A0 engineering INVALID: no-write 1.000, probes at ceiling ([errata v2](SUB_A0_ENGINEERING_ERRATA_v2.md)) |
| 6 | Freeze the regime and propose the A0 re-test |
| 7 | Park the A0 substrate. A new substrate proposal needs approval |
| 8 | Simulation of control arms only, plus the analytic predictions in §7 |
| 9 | Engineering / substrate validity |
| 10 | A regime fact about one fault family and one write physics. No learning, priority, or organizational claim |
| 11 | None directly. It prepares a C0/C1 prerequisite |
| 12 | O1/O2-related prerequisite. Arithmetic, write physics, topology and EXTERNAL repairers are all supplied |
| 13 | Whether the A0 negative pilot reflected a horizon artifact (prediction 3) or a substrate that cannot be identified |
