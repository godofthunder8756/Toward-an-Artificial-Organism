# SUB-A0 calibration results v1 (A0-cal stages 1–2)

2026-10-05. **STAGE 2 STOP: `PROBE_UNIDENTIFIABLE_STOP_AND_REPORT`.**
Stage 3 (holdout) was **not run**. The calibrated regime is **not frozen**. No
candidate arm was built, trained or evaluated, and no re-test is authorized.

## Provenance and approval basis

- Protocol: [SUB_A0_CAL_PROTOCOL_v1.md](SUB_A0_CAL_PROTOCOL_v1.md).
- Gate: [SUB_A0_VALIDITY_GATE_v1.json](SUB_A0_VALIDITY_GATE_v1.json).
- Harness: [sub_a0_cal_v1/](sub_a0_cal_v1/). All were committed by the user as
  `bcc0476` and frozen in [SUB_A0_CAL_FREEZE_v1.json](SUB_A0_CAL_FREEZE_v1.json)
  before any calibration seed ran.
- **Approval basis.** The user replied "Continue" to a report that requested freeze
  approval. An explicit confirmation was asked for and the user was unavailable.
  The freeze record states this inference. The protocol header still reads "DRAFT"
  because a hashed file cannot be edited; the freeze record is the authority.
- Raw outputs: [sub_a0_cal_results_v1/](sub_a0_cal_results_v1/). This holds
  per-job JSON, `.npz` trajectories (no pickle), manifests and summaries.
- **Replay:** stage-1 job (seed 2007, λ_e = 1) was recomputed from scratch and was
  identical in JSON and trajectory (`replay_identical: true`).
- 80 tests pass (24 A0-cal plus 56 earlier).

## Stage 1: regime grid (PASSED; selection made)

Of 24 cells × 13 horizons, 27 (cell, H) pairs were admissible. The registered
lexicographic rule selected:

**λ = (shrink 2, drift 1, erase 1), H = 2048.** This means A0's law with shrinkage
doubled, run for twice A0's horizon. The tie on departure 1 with (1, 2, 1) at
H = 2896 was broken by the shorter H.

| Quantity, calibration seeds 2000–2015 | Value |
| --- | --- |
| Median NO_MAINT retention at H | **0.668**, inside [0.60, 0.75] |
| Per-seed NO_MAINT | 0.664, 0.598, 0.668, 0.633, 0.691, 0.668, 0.711, 0.773, 0.742, 0.664, 0.621, 0.844, 0.586, 0.629, 0.793, 0.707 |
| Seeds with NO_MAINT < 0.90 | 16/16 |
| IMMORTAL | 1.000 on every seed |
| EXT_BISTABLE retention / gap recovery | 1.000 on every seed / median **1.000** |
| EXT_MEDIAN, matched (reference) | 0.777, recovery 0.33 |
| EXT_JUMP, A0 rule (reference) | 0.777 |

**Achievable range** over the whole grid:
- median NO_MAINT runs from 0.479 to 1.000;
- the repairability criterion holds across all of [0.479, 0.992];
- the highest median recovery is 1.000.

The window was reachable in many cells. Calibration did not have to push to
extremes.

### Registered predictions, scored

| # | Prediction | Outcome |
| --- | --- | --- |
| 1 | EXT_BISTABLE recovery degrades first at λ_s = 2 with high λ_d | **Partly wrong.** The worst cell was (2, 8, 32) at 0.708, consistent with the prediction. But λ_e = 32 lowered recovery in every λ_s, λ_d combination (0.71–0.85), an erasure effect the prediction did not name. No λ_s = 2, λ_e = 1 cell fell below 0.948 |
| 2 | EXT_MEDIAN below EXT_BISTABLE at every admissible pair | **Confirmed** (0 violations). Median-only repair cannot undo common-mode shrinkage |
| 3 | Pure horizon fix λ = (1, 1, 1), H ≈ 2896, NO_MAINT ≈ 0.64 | **Wrong in detail.** NO_MAINT at (1, 1, 1) was 0.938 at H = 2048, **0.758** at 2896 (0.008 above the window) and 0.580 at 4096. The mean-field model under-predicted retention by about 0.1. The direction was right: A0's failure is a timescale artifact, and the window falls between 2× and 4× the A0 horizon |
| 4 | W\* = 64; EXT closure ≈ 1; NO_MAINT closure ≈ 0; W = 16 fails | EXT closure 1.000 at W = 64 ✓. W = 16 fails ✓. **NO_MAINT closure 0.19, not ≈ 0 ✗.** This sinks stage 2 (below) |

**Natural lesions** (descriptive only, selected cell): single-region erase events
changed accuracy by less than 0.01 within 1,024 ticks in every arm. Erasing one
replica out of three barely moves a mean readout. **The pressure in this regime is
common-mode shrinkage plus drift, not lesions.**

## Stage 2: probe window (FAILED the registered criterion)

Selected cell, calibration seeds, K = 4 triggers per seed. All 64 lesions landed
on every trigger, so 16/16 seeds were eligible at every W.

| W | Median EXT_BISTABLE closure | Median NO_MAINT closure | EXT_MEDIAN (ref) | Admissible |
| ---: | ---: | ---: | ---: | --- |
| 16 | 0.000 | 0.014 | 0.314 | no (EXT < 0.75) |
| 64 | **1.000** | **0.191** | 0.830 | no (NO_MAINT > 0.10) |
| 256 | 1.000 | 0.355 | 0.941 | no |
| 1024 | 1.000 | 0.645 | 0.900 | no |

As registered: no W is admissible, so **STOP and report**. Stage 3 does not run.
No reselection was attempted.

### Diagnosis (exploratory, after the result; not a registered analysis)

In the NO_MAINT arm at W = 64:
- the **unlesioned parent's accuracy did not change** (median change 0.000);
- the **lesioned fork's accuracy rose** by a median of +0.045, with no repair at all.

The fork rose by +0.074 at W = 256. At W = 1024 the parent fell by 0.125, so
convergence adds to the effect there.

**Cause: a design error in my probe.** Setting one replica to −2.5 × the mean of
the other two gives a triplet mean of −(a+b)/12. That flips the readout but leaves
a margin of only about 1/12 of the remaining magnitude. Drift alone crosses back
over zero for a fraction of the lesioned bits. The NO_MAINT "closure" is
spontaneous reversal of a shallow lesion, not repair.

The separation itself is large: at W = 64, EXT closes 1.00 against NO_MAINT 0.19.
The registered absolute null bound (≤ 0.10) failed because the lesion was too
shallow, not because repair is unidentifiable in this regime.

**Protocol flaw, flagged.** Protocol §9 groups stage-2 failure with "the A0
substrate cannot host an identifiable maintenance contrast." That wording
overreaches for this outcome. Stage 1 shows the substrate does host a large,
fully repairable maintenance contrast. What failed is the specific probe. I do not
treat §9 as authority for a substrate conclusion here; the human decides (below).

## What is established, and what is not

- **Established (engineering, bounded):**
  - Under the A0 fault family at A0 write physics, a regime exists with real
    maintenance pressure: NO_MAINT 0.668 at H = 2048, with 16/16 seeds below the
    0.90 gate.
  - That regime is **fully** recoverable from surviving live redundancy by an
    invulnerable restoring organ: 16/16 seeds at 1.000.
  - It is only one-third recoverable by median-only repair.
  - A0's INVALID result is consistent with a timescale artifact.
- **Not established:**
  - an identifiable repair-capacity probe;
  - a holdout replication of the regime;
  - anything about learned repair, allocation, priority or dependence.

## Engineering observation that matters for any re-test (speculation, labelled)

The selected regime's damage is **common-mode shrinkage**: all three replicas
decay together. EXT_BISTABLE succeeds only because T is a bit table with one known
magnitude. Performing coefficients R are real-valued operator weights. No live
redundancy recovers a common-mode loss of their magnitude, because no reference
survives. Uneven regional modes also distort ratios between R coefficients. The
candidate's own machinery may therefore be **unrepairable in principle under this
regime**, unless its function lives in sign or ratio structure, or development
discovers a scale-robust code. If so, a re-test would end at row 1 or 2 (a
competence or maintenance-use NEGATIVE) for reasons this substrate fixes in
advance, not because dependence fails to produce priority. A cell with less
shrinkage would not escape this, since every admissible cell includes shrinkage.
This needs an analytic check before any re-test is proposed for freeze.

## Compute

| Stage | Wall | Worker wall total | Notes |
| --- | ---: | ---: | --- |
| Stage 1 | 4,291 s (cap 5,400) | 51,007 s ≈ 14.2 worker-h | About 1,110 s per job under 12-worker contention. The pre-run estimate was 6.1 CPU-h, so contention was underestimated |
| Stage 2 | 86 s | — | 16 jobs |
| Replay (1 job) | about 500 s | — | Identical |

CPU only, one thread per worker, PyTorch 2.7.0+cpu, Python 3.13.3. MACs, energy and
memory traffic were not measured.

## Decision needed (human)

| Option | What it is | What it would license |
| --- | --- | --- |
| **A (recommended)** | Probe v2 successor: deeper lesion (−4× mean of others, so the margin is (a+b)/3, 4× the v1 margin) with the **same** EXT ≥ 0.75 / NO_MAINT ≤ 0.10 criteria and W grid. Rerun stage 2 on calibration seeds (the regime selection is unchanged and the holdout is untouched), then stage 3 on the holdout. Predicted W\* = 256: restore distance ≈ 2m ≈ 8.9, about 178 bounded writes | Stage 3 PASS leads to a regime freeze proposal. **Before** any re-test freeze, the R-repairability analytic check (above) must also pass |
| B | Keep the v1 lesion and replace the absolute null bound with a differential one (EXT − NO_MAINT ≥ 0.50) | Same as A, but the criterion would be chosen **after seeing** stage-2 data. Only the untouched holdout could confirm it. Weaker; not recommended |
| C | Read §9 literally: park the A0 substrate | Ends this line on a probe-design error. I think this overstates the evidence |

No option licenses candidate training. The re-test still needs its own protocol,
development envelope, freeze and approval
([proposal](SUB_A0_RETEST_PROPOSAL_v1.md)).
