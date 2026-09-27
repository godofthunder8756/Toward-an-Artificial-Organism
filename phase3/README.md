# Phase-III (T3 / N2) implementation

The runnable realization of `ACI_PHASE3_PROTOCOL_v1.md` (G11's deliverable): the
Shared Latent Workspace candidate and its five reduction rivals R1–R5, the three
invariance-class specialists, the five canonical interventions I1–I5 plus the
π-cut and the leakage ablations, the coordination manifold, the novel-consumer
test, and the leakage audit — reusing the bridge harness (`.venv-bridge` torch
env, exact sign-flip stats, deterministic seeding).

## Layout

| Module | Role |
| --- | --- |
| `config.py` | `Phase3Config` — every frozen constant; the deferred values (δ, c, the S_plan cost model, θ's reactive form) fixed here as documented choices |
| `task.py` | G2 generative model (z, tokens, λ, probe), b-bit quantization, the true Bayes ceiling |
| `model.py` | `Encoder` (GRU, residual update) + `Maintenance` (paid refresh π + fixed/reactive A, no gradient) |
| `specialists.py` | S_pol / S_plan / S_reg fixed functions, the SPRT derivation, the manifold triples |
| `arms.py` | the six arms, `apply_specialists` (the wiring: shared vs private) |
| `train.py` | supervised training of the encoder (BCE) and R2/R3 heads |
| `interventions.py` | I1–I5, the single-write test, π-cut support |
| `leakage.py` | the capacity-capped z-decoder instrument |
| `novel_consumer.py` | S_conf / S_bias reuse + the Bayes ceiling |
| `runner.py` | train/evaluate/store/audit/replay driver |
| `audit.py` | audit (re-derive coverage + hashes without simulating) + replay + wiring checks |
| `run_engineering.py` | engineering entry point (`mkdir(exist_ok=False)`, snapshot, rows.jsonl) |
| `tests/` | 49 tests across the seven named areas (all green) |

## Run

```bash
cd ~/projects/Toward-an-Artificial-Organism
# CPU-only: the bridge is CPU-only by design; hide the GPU or a loaded DGX
# Spark GPU will OOM on the first CUDA context (see G12's engineering screen).
export CUDA_VISIBLE_DEVICES=
export OPENBLAS_NUM_THREADS=1
PYTHONPATH=. .venv-bridge/bin/python -m pytest phase3/tests -q      # 50 tests
# Each --seeds entry is a *model seed* (fresh training + its own eval stream).
PYTHONPATH=. .venv-bridge/bin/python -B phase3/run_engineering.py \
    --out phase3_results_engineering_v1 --seeds 0 1 2 3 4 5 6 7
```

## Design decisions fixed at implementation (protocol-deferred values)

- **Decay δ = 1.0, refresh cost c = 1.0** (G0 §3.6). The maintained workspace
  relaxes toward neutral at rate δ each unrefreshed step and π (cost c) holds
  it. δ = 1.0 makes persistence *paid in the strong sense* (N1's "refresh nearly
  every tick"): cutting π leaves the probe belief at chance (0.500), while the
  maintained arm holds the full accumulation (~0.97). This is the N1 countdown
  with lifetime 1/δ = 1, stated as the graded leak.
- **Maintenance rule A** (verdict D) is `refresh iff E >= c` (energy-gated,
  z-blind, reads (s, E, d) only). It never reads W (L3).
- **Encoder residual form** W_t = W_{t-1} + head(GRU(h_{t-1}, [x_t; W_{t-1}])):
  the GRU learns the *increment* (the λ mapping), the running sum is carried
  structurally by the W feedback. The workspace h_t leaks at rate δ after the
  readout, so a π-cut (or F1's zeroed W) leaves h_t unable to accumulate z
  independently — MAINTAINED is testable rather than asserted.
- **S_plan cost model** (G3 §2.2, deferred): R_correct = R_wrong = 1, c_obs =
  0.1, abstain 0. The SPRT boundaries a = b ≈ 0.97 are *derived* by value
  iteration before training (`sprt_boundaries`), never tuned.
- **S_reg θ** (G6 §2.3): reactive, clamped to [θ_lo, a] with θ_base = 0.5 < a,
  so the manifold has exactly six realizable triples.

## Notable corrections vs the frozen protocol text

- **The protocol's "Bayes ceiling 0.812" is the Chernoff *bound* 1 − exp(−t·C)**,
  a loose lower bound on accuracy at finite t (the table's own t=4 entry is
  0.243, below chance, which is impossible for a Bayes decision). The true
  Bayes-optimal accuracy of sign(S_H) for this model is ~0.97 (drift 0.288/step
  × 24 steps = 6.9 nats mean |S|). The implementation uses the *empirical*
  ceiling (`task.true_bayes_ceiling`) as the equivalence anchor and reports
  0.812 as the documented bound; the protocol's numeric anchor is not silently
  rewritten.
- The b-bit resolution ≈ 0.39 is *coarser* than λ_lo = 0.35 (the protocol says
  "finer"); the frozen value b = 5 over [−6,+6] is implemented literally.

## Arm accuracy (engineering, 2000 steps, per-arm probe accuracy ≈ Bayes ceiling)

candidate 0.97 · R1 0.96 · R2 0.96 · R3 0.93 · R4 0.97 · R5 0.97. Incoherence
rate: candidate/R4/R5 = 0 by construction; R1 > 0 (measured); R2/R3 empirical.
π-cut collapses the candidate probe to 0.500; F1 (π-cut + zero W) leaves h_t at
chance (decode 0.498).

No autopoiesis or consciousness claim. This is an implementation of a frozen
protocol, not a result.
