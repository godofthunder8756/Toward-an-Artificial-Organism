"""Smoke tests for the bridge reproducibility harness.

Runs both as a pytest module (``pytest bridge/tests/``) and as a plain script
(``.venv-bridge/bin/python bridge/tests/test_harness.py``), so the harness can
be verified against a bare venv before torch/pytest are installed.
"""

from __future__ import annotations

import os
import random
import tempfile

from bridge.config import BridgeConfig
from bridge.episodes import save_episodes, load_episodes
from bridge.reproducibility import seed_all, available_backends


def test_config_json_roundtrip():
    cfg = BridgeConfig()
    cfg2 = BridgeConfig.from_json(cfg.to_json())
    assert cfg2 == cfg
    # nested reconstruction, not just dict identity
    assert cfg2.arch.gru_hidden == cfg.arch.gru_hidden == 16


def test_config_dict_roundtrip():
    cfg = BridgeConfig()
    assert BridgeConfig.from_dict(cfg.to_dict()) == cfg


def test_config_yaml_roundtrip():
    cfg = BridgeConfig()
    assert BridgeConfig.from_yaml(cfg.to_yaml()) == cfg


def test_default_yaml_matches_defaults():
    import importlib.util
    if importlib.util.find_spec("yaml") is None:
        return  # PyYAML absent; JSON fallback already covered above
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "configs", "default.yaml")
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    assert BridgeConfig.from_yaml(text) == BridgeConfig()


def test_parameter_counts_positive():
    counts = BridgeConfig().parameter_counts()
    for name, n in counts.items():
        assert isinstance(n, int) and n >= 0, (name, n)
    assert counts["total"] == sum(v for k, v in counts.items() if k != "total")
    assert counts["gru"] > 0


def test_seed_reproducible():
    seed_all(1234)
    a = [random.random() for _ in range(5)]
    seed_all(1234)
    b = [random.random() for _ in range(5)]
    assert a == b


def test_available_backends_shape():
    be = available_backends()
    assert be["python"] is True
    assert isinstance(be["numpy"], bool)
    assert isinstance(be["torch"], bool)


def test_episode_roundtrip():
    episodes = [
        [{"t": 0, "obs": [0, 1], "action": "refresh", "reward": 0.0},
         {"t": 1, "obs": [1, 0], "action": "hold", "reward": 1.0}],
        [{"t": 0, "obs": [0, 0], "action": "hold", "reward": 0.0}],
    ]
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
        path = fh.name
    try:
        assert save_episodes(path, episodes) == 2
        loaded = load_episodes(path)
        assert loaded == episodes
    finally:
        os.unlink(path)


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"OK: {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
