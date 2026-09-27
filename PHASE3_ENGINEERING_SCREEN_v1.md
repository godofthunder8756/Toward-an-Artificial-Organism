# Phase-III engineering screen v1 — G12

2026-09-27. Deliverable for the G12 card (`t_89b71174`): *does the implementation
pass engineering screening under a declared finite search budget (no
candidate-must-win)?*

**Verdict: GO.** All seven "may verify" items pass on the engineering seed
family (0–7), under the declared budget below. The implementation and the final
seeds (100–111) are frozen; the frozen engineering artifact and its snapshot are
the deliverable. This screen establishes that the phase3 implementation is
*wired correctly and learnable*, not that the candidate beats any rival or that
H4/H5 hold — those are final scientific results and belong to G13.

This document is a screen report, not a result. It makes no autopoiesis,
consciousness, or level-(d)/(e) claim.

---

## 1. Declared search budget (fixed before any measurement)

- **Frozen default**: `p_level = small` (GRU hidden 8), `steps = 2000`, `lr = 1e-3`,
  xavier init, Adam. All six arms, engineering model seeds 0–7.
- **Sweep** (learnability robustness only): `p_level ∈ {small, mid}` ×
  `steps ∈ {1000, 2000}`, **candidate arm only**, engineering seeds 0–1 — eight
  configurations. This is the entire tuning allowance; it exists to confirm the
  latent task is learnable and not knife-edge, and to confirm the candidate does
  **not** systematically beat the ceiling (a wiring bug's signature), never to
  make sharing win.
- **No lr / init / optimizer tuning** beyond the frozen `TrainingConfig` defaults.
- Engineering seeds 0–7 are excluded from every final sample; finals are the
  disjoint family 100–111 (12 seeds), the frozen `SeedConfig.final_seeds`.

## 2. The seven "may verify" items — all pass

Measured on the frozen-default configuration (`small`/2000), model seed 0,
evaluation seed 999, 1024 balanced episodes (the screen stream), plus the frozen
8-seed run for V1/V4/V5.

| # | Item | Measured result | Verdict |
| --- | --- | --- | --- |
| V1 | latent task learnable | candidate probe acc 0.942–0.982 across the 8 engineering seeds; on the screen stream 0.971 vs R4 ceiling 0.974 (candidate − ceiling = −0.003, no beat) | PASS |
| V2 | specialists individually learnable | R2 heads match specialist targets {spol 0.996, splan 0.991, sreg 0.992}; R3 {0.996, 0.997, 0.955} | PASS |
| V3 | interventions function | I1 scramble signature traces (S_pol, S_plan, S_reg)(w★) exactly for w★ ∈ {−3.0, −0.4, +0.4, +3.0} | PASS |
| V4 | coordination non-vacuous | incoherence: candidate = 0.000 (8/8 seeds), R1 = 0.0028–0.0293 > 0 (8/8), R4/R5 = 0 (by construction), R2/R3 empirical (0.0007–0.0207) | PASS |
| V5 | candidate + rivals train | all six arms reach the ceiling: probe acc 0.94–0.98 per seed across candidate/R1/R2/R3/R4/R5 | PASS |
| V6 | hidden-copy controls work | F1 free-recurrence decode = 0.482 (chance); weight-bypass (I2-scramble→0) decode = 0.500 (chance) | PASS |
| V7 | no leakage breaks W attribution | sever (specialists are pure functions of W, source-level); decode-ablation: h_t decode 0.965 vs zeroed-pathway 0.482 | PASS |

**Learnability sweep (all eight configurations, candidate arm).** Probe accuracy
0.965–0.976 across `{small, mid} × {1000, 2000}` on seeds 0–1 — every
configuration reaches the empirical ceiling (~0.963–0.974); the frozen default
is not knife-edge, and no configuration beats the ceiling by more than noise.

**Paid persistence (V1 companion, H1.3 pre-check).** The π-cut collapses the
candidate/R1 probe to exactly 0.500 on every one of the 8 seeds; R4/R5 (free
accumulator, no π) are unchanged by the cut — the maintained-vs-free contrast is
present and correct at the engineering screen.

## 3. Defects found and fixed (the screen's job)

Five defects were found by the screen and fixed before freezing. None was a
scientific result; all were wiring/config/test-harness defects.

1. **S_plan encoding mismatch (real bug).** `phase3/train.py:specialist_targets`
   encoded the S_plan target as postpone=1, commit-B=2, but
   `phase3/specialists.py:s_plan` uses `COMMIT_A=0, COMMIT_B=1, POSTPONE=2`.
   The R2/R3 heads were therefore trained to output "postpone" where the fixed
   function says "commit-B", corrupting the R2/R3 incoherence endpoint (an
   AC14-class silent-wiring defect). Fixed by importing the named constants and
   aligning the target encoding; a regression test
   (`test_specialist_targets_splan_encoding_matches_s_plan`) now pins the two
   encodings together.
2. **Driver defaults contradicted the frozen config.** `run_engineering.py`
   defaulted `--steps 200` / `--n-episodes 512` against the frozen
   `TrainingConfig.steps=2000` / `SeedConfig.eval_episodes_per_seed=1024`.
   Fixed to the frozen values.
3. **Driver under-counted the model seed.** `run_engineering.py` trained one
   model and re-evaluated it across episode seeds; protocol §10.1 makes the
   *model seed* the replication unit (one draw of training RNG **and** the
   eval stream). Fixed to retrain a fresh six-arm model per seed.
4. **Test harness was order-dependent.** `phase3/tests/conftest.py` created
   `Encoder()` with an unseeded xavier init, so the session encoder's weights —
   and hence the borderline `test_s_conf_reaches_bayes_ceiling` result — varied
   with pytest run order (a "pin ambient module state" failure). Fixed by
   seeding before init; the session encoder is also now trained at the frozen
   2000 steps (400 steps under-trained calibration and sat the log-loss
   assertion right at its threshold). The suite is byte-deterministic in both
   forward and reverse order.
5. **Environment.** This host's GPU is reserved by the running inference
   servers, and the `.venv-bridge` torch wheel is a `+cu130` build, so an
   un-hidden GPU OOMs on the first CUDA context. The bridge is CPU-only by
   design; the fix is `CUDA_VISIBLE_DEVICES=` (now documented in the README and
   all run commands), not any code change.

## 4. The freeze

- **Frozen engineering artifact**: `phase3_results_engineering_v1/` — 48 rows
  (6 arms × 8 engineering seeds), `pre_run_snapshot.json` (sha256 of the ten
  phase3 simulation sources + `ACI_PHASE3_PROTOCOL_v1.md`), `rows.jsonl`,
  `results.json` (`state_hash`
  `9d689165857a38cd921eb155ae61f61a2a0219b4a0fd16e52f9aa8def41f75e2`).
  `mkdir(exist_ok=False)` — never overwritten.
- **Final seeds**: 100–111 (12), frozen in `SeedConfig.final_seeds`, disjoint
  from engineering 0–7. The runner asserts the run's seeds equal the declared
  engineering family (they do: `[0..7]`).
- **Audit**: `phase3/audit.py:audit_results` re-derives 48/48 coverage, all
  six arms × all eight seeds (no missing arm-seed), and the recorded state hash
  equals the recomputed hash. The 51-test suite (50 + the new encoding
  regression test) is green in forward and reverse order.
- **Verification tools are not hashed** (AC16/17 discipline): `run_engineering.py`,
  `screen.py`, and `phase3/tests/*` are excluded from the snapshot; the frozen
  source of truth is the protocol + the ten simulation modules.

## 5. What is NOT claimed here

- No claim that the candidate beats R1 / R2 / R3 / R4 / R5 — that is G13's
  final question, gated by H1–H5 and the frozen statistical plan.
- No H4/H5 pass, and no tuning of the world so sharing wins. The only contrast
  this screen asserts is the *structural* one (single-W coherence = 0 vs
  R1's private-copy incoherence > 0) plus learnability, both of which hold by
  construction and are verified, not tuned.
- The protocol's "Bayes ceiling 0.812" is the Chernoff bound; the empirical
  ceiling (~0.963 at 20k episodes, ~0.974 on the 1024-episode screen stream) is
  used as the equivalence anchor, exactly as G11 flagged for G12.

## 6. Handoff to G13

The implementation and final seeds are frozen. G13 may run the finals on seeds
100–111 untouched:

```
export CUDA_VISIBLE_DEVICES=
export OPENBLAS_NUM_THREADS=1
PYTHONPATH=. .venv-bridge/bin/python -B phase3/run_engineering.py \
    --out phase3_results_finals_v1 --seeds 100 101 102 103 104 105 106 107 108 109 110 111
```

G13 must gate H1.2/H5.2 equivalence on the **empirical** ceiling (R4's measured
probe accuracy on the finals stream), never on the 0.812 bound.
