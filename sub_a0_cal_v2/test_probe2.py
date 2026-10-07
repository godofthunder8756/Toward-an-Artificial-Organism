from __future__ import annotations

from pathlib import Path

import pytest
import torch

from sub_a0_v1.model import Layout, TASK_BITS
from sub_a0_cal_v1 import arms
from sub_a0_cal_v1.arms import acquire, accuracy, initial_values, perturb, probe_draws, repair
from sub_a0_cal_v2 import probe2

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SEED = 9001


def test_engineering_seeds_are_disjoint_from_registered_sets() -> None:
    registered = set(range(8)) | set(range(1000, 1032)) | set(range(2000, 2016)) | set(range(2100, 2116))
    assert not set(probe2.ENGINEERING_SEEDS) & registered
    assert FIXTURE_SEED not in probe2.ENGINEERING_SEEDS
    assert probe2.APPROVED_DEPTH in probe2.DEPTHS


@pytest.mark.parametrize("depth", probe2.DEPTHS)
def test_depth_override_sets_lesion_and_keeps_flip_and_recoverability(depth: float) -> None:
    layout = Layout.create(FIXTURE_SEED)
    task, labels = acquire(FIXTURE_SEED)
    values = initial_values(layout, task)
    order, replica = probe_draws(FIXTURE_SEED, 0)
    saved = arms.PROBE_REVERSAL
    try:
        arms.PROBE_REVERSAL = depth
        lesioned, used = perturb(values, layout, labels, order, replica)
    finally:
        arms.PROBE_REVERSAL = saved
    assert arms.PROBE_REVERSAL == -2.5
    assert used == arms.PROBE_FRACTION_COUNT
    changed = (lesioned != values).nonzero().flatten()
    assert torch.allclose(lesioned[changed], depth * values[changed])
    assert float(accuracy(lesioned, layout, labels)) == pytest.approx(1 - used / TASK_BITS)
    for _ in range(1200):
        lesioned, _ = repair(lesioned, "ext_bistable", layout)
    assert float(accuracy(lesioned, layout, labels)) == 1.0


def test_depth_selection_rule() -> None:
    assert probe2.choose_depth({-3.0: None, -4.0: None}) is None
    assert probe2.choose_depth({-3.0: 0.05, -4.0: 0.2, -5.0: 0.1, -6.0: None}) == -4.0
    assert probe2.choose_depth({-3.0: 0.2, -4.0: 0.2, -5.0: 0.2}) == -4.0
    assert probe2.choose_depth({-3.0: 0.2, -5.0: 0.2}) == -5.0  # equidistant: lower value
    stats = {"selected_window": 256, "windows": {"256": {"medians": {"ext_bistable": 1.0, "no_maint": 0.04}}}}
    assert probe2.depth_margin(stats) == pytest.approx(0.06)
    assert probe2.depth_margin({"selected_window": None}) is None


def test_v2_runner_refuses_without_its_own_freeze() -> None:
    if (ROOT / probe2.FREEZE).exists():
        pytest.skip("Probe-v2 freeze exists; refusal path not applicable")
    with pytest.raises(RuntimeError):
        probe2.require_freeze()


def test_v2_never_references_candidate_machinery() -> None:
    source = (ROOT / "sub_a0_cal_v2" / "probe2.py").read_text(encoding="utf-8")
    for token in ("propose", "training_step", "intercept", "meta_"):
        assert token not in source
