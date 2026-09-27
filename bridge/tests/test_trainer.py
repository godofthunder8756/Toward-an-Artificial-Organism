"""Acceptance tests for the training loop, losses, and gradient paths (N9).

Verifies the task's acceptance criteria:

1. The trainer imports cleanly.
2. A small training run completes on CPU and logs finite loss + economy
   metrics (energy, age, alive fraction, refresh rate) every step.
3. Each loss term flows gradient to exactly its intended component and
   nowhere else (the N4 §7.3 gradient-path table, checked at the gradient
   level).
4. A training step changes the parameters (gradients are applied).
5. Two same-seed trainers are deterministic (identical step-0 metric digest).
6. Saved evaluation episodes round-trip (same environment reused across arms).
7. Checkpoints round-trip.
8. No CUDA is referenced in the new sources.

Runs as pytest (``pytest bridge/tests``) or as a plain script
(``.venv-bridge/bin/python -B bridge/tests/test_trainer.py``).
"""

from __future__ import annotations

import os
import re
import tempfile

import torch

from bridge.agent import NeuralBridge
from bridge.config import BridgeConfig
from bridge.env import BridgeEnv
from bridge.trainer import BridgeTrainer, compute_losses

NEW_SOURCES = [
    "bridge/trainer.py",
    "bridge/env.py",
    "bridge/run.py",
]

_CUDA_API = re.compile(
    r"torch\.cuda|\.cuda\(|cuda:\d+|['\"]cuda['\"]|\.to\(['\"]cuda"
)


def _source_paths():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return [os.path.join(repo_root, p) for p in NEW_SOURCES]


def _component(named_grads):
    """Map parameter-name prefixes with non-zero grad to a coarse component."""
    comps = set()
    for name in named_grads:
        if name.startswith("controller."):
            comps.add("gru")
        elif name.startswith("v_estimator."):
            comps.add("f_V")
        elif name.startswith("allocator.policy"):
            comps.add("A_policy")
        elif name.startswith("allocator.critic"):
            comps.add("A_critic")
        elif name.startswith("probe."):
            comps.add("S_pol")
        else:
            comps.add(name)
    return comps


def _grad_components(bridge, loss):
    bridge.zero_grad()
    loss.backward()
    names = {
        n
        for n, p in bridge.named_parameters()
        if p.grad is not None and p.grad.abs().sum() > 0
    }
    return _component(names)


def test_trainer_imports_cleanly():
    import bridge  # noqa: F401
    from bridge.trainer import BridgeTrainer, compute_losses  # noqa: F401
    from bridge.env import BridgeEnv  # noqa: F401


def test_small_training_run_completes_on_cpu():
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=0)
    history = trainer.train(steps=4, batch_size=8)

    assert len(history) == 4
    required = {
        "total", "L_V", "J_A_policy", "J_A_critic", "probe",
        "mean_energy", "mean_age", "alive_frac", "refresh_rate",
    }
    for step, row in enumerate(history):
        assert required <= set(row), (step, row.keys())
        assert row["step"] == step
        for k in required:
            assert torch.isfinite(torch.tensor(row[k])), (step, k, row[k])
    # Economy is simulated: energy and age are recorded and finite.
    assert all(row["mean_energy"] >= 0.0 for row in history)


def test_training_step_changes_parameters():
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=1)
    before = {n: p.detach().clone() for n, p in trainer.bridge.named_parameters()}
    batch = trainer.env.sample(8)
    trainer.step(batch)
    for n, p in trainer.bridge.named_parameters():
        assert not torch.equal(before[n], p), f"parameter {n} did not change"


def test_gradient_paths_match_protocol():
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=2)
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    losses, _ = compute_losses(cfg, out, batch)

    # L_V -> f_V and GRU only (content-blind); never A or S_pol.
    lv = _grad_components(trainer.bridge, losses["L_V"])
    assert lv == {"f_V", "gru"}, lv

    # J_A policy gradient -> A_policy only (V->A edge stop-gradiented).
    jp = _grad_components(trainer.bridge, losses["J_A_policy"])
    assert jp == {"A_policy"}, jp

    # J_A critic -> A_critic only.
    jc = _grad_components(trainer.bridge, losses["J_A_critic"])
    assert jc == {"A_critic"}, jc

    # probe reward gradient -> S_pol only (W content detached; no cue leakage
    # to the GRU, V, or A).
    pr = _grad_components(trainer.bridge, losses["probe"])
    assert pr == {"S_pol"}, pr


def test_determinism_same_seed():
    cfg = BridgeConfig()
    a = BridgeTrainer(cfg, seed=7)
    b = BridgeTrainer(cfg, seed=7)
    ha = a.train(steps=3, batch_size=8)
    hb = b.train(steps=3, batch_size=8)
    for ra, rb in zip(ha, hb):
        assert ra == rb, (ra, rb)


def test_eval_episodes_roundtrip():
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    trainer = BridgeTrainer(cfg, seed=3)
    batch = trainer.env.sample(8)

    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
        path = fh.name
    try:
        n = trainer.save_eval_episodes(batch, path)
        assert n == 8
        reloaded = trainer.load_eval_episodes(path)
        for key in ("x", "cue", "regime", "regime_class", "correct"):
            assert torch.equal(batch[key], reloaded[key]), key
    finally:
        os.unlink(path)


def test_checkpoint_roundtrip():
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=4)
    trainer.train(steps=2, batch_size=4)

    with tempfile.NamedTemporaryFile("w", suffix=".pt", delete=False) as fh:
        path = fh.name
    try:
        trainer.save_checkpoint(path)
        restored = BridgeTrainer.load_checkpoint(path)
        for n, p in trainer.bridge.named_parameters():
            assert torch.equal(p, restored.bridge.state_dict()[n]), n
    finally:
        os.unlink(path)


def test_no_cuda_referenced():
    for path in _source_paths():
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        hits = _CUDA_API.findall(text)
        assert not hits, f"{path} references CUDA: {hits}"


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"OK: {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
