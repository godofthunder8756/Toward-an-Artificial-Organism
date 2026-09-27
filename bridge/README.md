# Bridge reproducibility harness

Shared, version-controlled substrate for the neural-bridge study line
(`ACI_BRIDGE_PROTOCOL_v3.md`). One venv + one config object + one seed
specifies a whole run.

## Layout

- `bridge/config.py` — `BridgeConfig` dataclass (architecture, energy, decay,
  optimizer, losses, gradient paths) with YAML/JSON serialization and a
  `parameter_counts()` helper.
- `bridge/reproducibility.py` — `seed_all(seed)` and `deterministic_context`
  (pins Python/NumPy/torch RNGs; NumPy/torch seeded only when importable).
- `bridge/episodes.py` — `save_episodes` / `load_episodes` / `EpisodeRecorder`
  (stdlib JSONL) so every arm reuses the same saved evaluation episodes.
- `bridge/modules.py` — the six neural modules of the frozen v3 protocol
  (Controller GRU, Workspace W, IntegrityEstimator V, MaintenanceAllocator A,
  ProbeReadout S_pol, RefreshAction pi), CPU-only torch.
- `bridge/substrate.py` — `Substrate`: the resource-economy / decay
  bookkeeping law (energy, budget, decay age, refresh effect; no gradient).
- `bridge/agent.py` — `NeuralBridge`: wires the modules to the substrate and
  runs a batch forward pass on CPU; `actual_parameter_counts()` reports the
  real torch parameter counts keyed like `BridgeConfig.parameter_counts()`.
- `bridge/env.py` — `BridgeEnv`: generates the c-independent environment
  (distractor stream, one-shot cue in `{+1, -1}`, announced regime, exogenous
  metabolic-correctness stream) and round-trips batches through the
  `episodes` JSONL format so every arm reuses the same episodes.
- `bridge/trainer.py` — `BridgeTrainer`: the CPU training loop. Realizes the
  exact v3 §7 / N4 objectives — `L_V` (supervised estimator), `J_A`
  (REINFORCE with a learned baseline over the homeostatic cost), probe NLL —
  with per-component learning-rate groups and the protocol's gradient paths.
- `bridge/run.py` — reproducible run entry point: trains, emits the
  architecture/training/energy/decay records, saves metrics, checkpoint, and
  eval episodes, and verifies determinism by re-running the same seed.
- `bridge/configs/default.yaml` — reference default (mirrors the dataclass
  defaults; parsed by `BridgeConfig.from_yaml` when PyYAML is present).
- `bridge/tests/test_harness.py` — harness smoke tests (runs as pytest or as a
  script); `bridge/tests/test_modules.py` — module acceptance tests;
  `bridge/tests/test_trainer.py` — training-loop, loss, gradient-path, and
  determinism acceptance tests; `bridge/tests/test_invariants.py` — the bridge
  invariants (W decay, paid refresh, energy conservation, reward separation,
  trainer-label severance, cue leakage, intervention correctness, deterministic
  replay).

## Environment

The venv is `.venv-bridge` at the repo root (Python 3.12.3), created with:

    uv venv .venv-bridge --python 3.12
    uv pip install --python .venv-bridge/bin/python torch numpy pyyaml pytest

torch is a CUDA-capable wheel (2.14.0+cu130) but the modules are **CPU-only by
construction**: nothing references CUDA, forward runs on CPU tensors, and every
parameter is on the CPU device (asserted by `test_no_cuda_referenced` and
`test_all_parameters_on_cpu`). Verify:

    .venv-bridge/bin/python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

## Running the harness (stdlib-only, no packages needed)

    cd <repo-root>
    PYTHONPATH=. .venv-bridge/bin/python -B bridge/tests/test_harness.py

## Running the test suite (once torch/pytest are installed)

    cd <repo-root>
    .venv-bridge/bin/python -m pytest bridge/tests -q

or, with uv project resolution:

    cd <repo-root>/bridge
    UV_PROJECT_ENVIRONMENT=$PWD/../.venv-bridge uv run pytest

## Running a training run

    cd <repo-root>
    PYTHONPATH=. .venv-bridge/bin/python -B bridge/run.py \
        --seed 0 --steps 20 --batch-size 16

The run writes `bridge/runs/bridge-<seed>/` (`run_record.json`, `metrics.jsonl`,
`checkpoint.pt`, `eval_episodes.jsonl`) and exits non-zero if the determinism
check fails. `bridge/runs/` is scratch output (gitignored), not a research
artifact.

## Reproducibility contract

- Seeds are the replication unit; engineering seeds are excluded from the final
  sample (disjoint families).
- A run is `seed_all(seed)` + `BridgeConfig` + the same environment + the same
  saved episodes. Nothing else may change the draw sequence.
- Every parameter (dims, optimizer, learning rates, init, seeds, steps,
  horizon, losses, gradient paths, energy, decay) is recorded in the config and
  therefore in the run's frozen `pre_run_snapshot`.
