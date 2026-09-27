"""Acceptance tests for the neural bridge modules (N9).

Verifies the task's acceptance criteria:

1. The modules import cleanly (implicit: this module imports them).
2. A dummy batch forward pass runs on CPU and returns the expected shapes.
3. Parameter counts are logged from the config and match the actual torch
   parameters exactly.
4. No CUDA is referenced anywhere in the module sources, and every parameter /
   output tensor lives on the CPU.

Runs as pytest (``pytest bridge/tests``) or as a plain script
(``.venv-bridge/bin/python -B bridge/tests/test_modules.py``).
"""

from __future__ import annotations

import os
import re

import torch

from bridge.config import BridgeConfig
from bridge.agent import NeuralBridge

MODULE_SOURCES = [
    "bridge/modules.py",
    "bridge/substrate.py",
    "bridge/agent.py",
]

# CUDA *API usage* patterns — not the word "CUDA" (docstrings may mention it in
# the negative). Any real CUDA reference in code matches one of these.
_CUDA_API = re.compile(
    r"torch\.cuda|\.cuda\(|cuda:\d+|['\"]cuda['\"]|\.to\(['\"]cuda"
)


def _source_paths():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return [os.path.join(repo_root, p) for p in MODULE_SOURCES]


def _dummy_batch(cfg: BridgeConfig):
    B, T = 4, cfg.episode.horizon_t
    x = torch.randn(B, T, cfg.arch.distractor_dim)
    cue = torch.randint(0, 2, (B, cfg.arch.w_bits)).float()
    regime = torch.nn.functional.one_hot(
        torch.randint(0, cfg.arch.regime_dim, (B, T)), cfg.arch.regime_dim
    ).float()
    correct = torch.randint(0, 2, (B, T)).bool()
    return x, cue, regime, correct


def test_modules_import_cleanly():
    import bridge  # noqa: F401
    from bridge.modules import (  # noqa: F401
        Controller,
        Workspace,
        IntegrityEstimator,
        MaintenanceAllocator,
        ProbeReadout,
        RefreshAction,
    )
    from bridge.substrate import Substrate  # noqa: F401
    from bridge.agent import NeuralBridge  # noqa: F401


def test_dummy_forward_pass_on_cpu():
    cfg = BridgeConfig()
    bridge = NeuralBridge(cfg)
    x, cue, regime, correct = _dummy_batch(cfg)

    out = bridge(x, cue, regime, correct)

    B, T = x.shape[:2]
    assert out["probe_logits"].shape == (B, 2)
    assert out["v"].shape == (B, T, cfg.arch.v_energy_bits + cfg.arch.v_integrity_bits)
    assert out["refresh"].shape == (B, T)
    assert out["energy"].shape == (B, T)
    assert out["age"].shape == (B, T)
    assert out["slot"].shape == (B, T, cfg.arch.w_bits)
    assert out["h"].shape == (B, T, cfg.arch.gru_hidden)

    # Everything stays on CPU.
    for name, tensor in out.items():
        assert tensor.device.type == "cpu", (name, tensor.device)


def test_parameter_counts_match_config():
    cfg = BridgeConfig()
    bridge = NeuralBridge(cfg)

    config_counts = cfg.parameter_counts()
    actual_counts = bridge.actual_parameter_counts()

    print("\nparameter counts (from config):")
    for name, n in config_counts.items():
        print(f"  {name:9s} {n}")
    print("parameter counts (actual torch):")
    for name, n in actual_counts.items():
        print(f"  {name:9s} {n}")

    for name in ("gru", "f_V", "A_policy", "A_critic", "S_pol", "total"):
        assert actual_counts[name] == config_counts[name], name


def test_no_cuda_referenced():
    for path in _source_paths():
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        hits = _CUDA_API.findall(text)
        assert not hits, f"{path} references CUDA: {hits}"


def test_all_parameters_on_cpu():
    bridge = NeuralBridge(BridgeConfig())
    for name, p in bridge.named_parameters():
        assert p.device.type == "cpu", name


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"OK: {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
