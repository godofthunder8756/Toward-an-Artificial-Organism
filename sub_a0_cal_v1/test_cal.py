from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import torch

from sub_a0_v1.model import (
    BUDGET, DESTINATIONS, REPAIR_COEFFICIENTS, TASK_BITS, Layout, State, select, task_logits,
)
from sub_a0_v1.world import FaultStream, damage
from sub_a0_cal_v1 import arms, calibrate, law
from sub_a0_cal_v1.arms import (
    BISTABLE_MAGNITUDE, ProbeSpec, accuracy, acquire, closure, gap_recovery,
    initial_values, perturb, probe_draws, repair, simulate,
)
from sub_a0_cal_v1.law import Cell, ParamFaultStream, apply, cell_terms

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SEED = 9001  # engineering fixture seed: not a calibration/holdout/A0 seed


def test_fixture_seed_is_disjoint_from_registered_seed_sets() -> None:
    registered = set(calibrate.CAL_SEEDS) | set(calibrate.HOLDOUT_SEEDS)
    registered |= set(range(8)) | set(range(1000, 1032))
    assert FIXTURE_SEED not in registered
    assert not set(calibrate.CAL_SEEDS) & set(calibrate.HOLDOUT_SEEDS)


def test_unit_multipliers_reproduce_a0_fault_stream_bitwise() -> None:
    old, new = FaultStream(50000), ParamFaultStream(50000, erase=1)
    cells = [Cell(1, 1, 1)]
    for _ in range(3000):
        expected, raw = old.next(), new.next()
        shrink, drift = cell_terms(raw, cells)
        assert torch.equal(shrink[0], expected.shrink)
        assert torch.equal(drift[0], expected.drift)
        assert torch.equal(raw.erase, expected.erase)


def test_damage_matches_a0_and_multipliers_only_scale() -> None:
    gen = torch.Generator().manual_seed(3)
    values = torch.randn(DESTINATIONS, generator=gen)
    old, new = FaultStream(77), ParamFaultStream(77, erase=1)
    for _ in range(50):
        fault = old.next()
        raw = new.next()
        shrink, drift = cell_terms(raw, [Cell(1, 1, 1), Cell(2, 4, 1)])
        batched = apply(values.repeat(2, 1, 1), shrink, drift, raw.erase)
        expected = damage(State(values, torch.zeros(DESTINATIONS, 4)), fault).values
        assert torch.equal(batched[0, 0], expected)
        assert torch.allclose(shrink[1], 2 * shrink[0])
        assert torch.allclose(drift[1], 4 * drift[0])
        values = expected


def test_erase_multiplier_raises_event_rate() -> None:
    counts = []
    for erase in (1, 32):
        stream = ParamFaultStream(5, erase=erase)
        counts.append(sum(stream.next().erase_event for _ in range(4000)))
    assert counts[1] > counts[0]


def test_acquisition_matches_a0_engineering_checkpoint_and_is_constant_magnitude() -> None:
    task, labels = acquire(0)
    with np.load(ROOT / "sub_a0_engineering_v1" / "acquired_0.npz", allow_pickle=False) as saved:
        assert np.array_equal(task.numpy(), saved["task"])
        assert np.array_equal(labels.numpy(), saved["evaluator_labels"])
    for seed in (0, FIXTURE_SEED, 12345):
        task, labels = acquire(seed)
        assert torch.all(task.abs() == BISTABLE_MAGNITUDE)
        assert torch.equal(task > 0, labels.bool())


def test_accuracy_matches_a0_readout() -> None:
    layout = Layout.create(FIXTURE_SEED)
    task, labels = acquire(FIXTURE_SEED)
    values = initial_values(layout, task) + 3 * torch.randn(DESTINATIONS)
    state = State(values, torch.zeros(DESTINATIONS, 4))
    expected = ((task_logits(state, layout) > 0) == labels.bool()).float().mean()
    assert torch.equal(accuracy(values, layout, labels), expected)


@pytest.mark.parametrize("kind", ["ext_bistable", "ext_median"])
def test_matched_external_arms_obey_candidate_write_physics(kind: str) -> None:
    layout = Layout.create(FIXTURE_SEED)
    values = 4 * torch.randn(3, DESTINATIONS)
    updated, changed = repair(values, kind, layout)
    delta = updated - values
    assert delta.abs().max() <= arms.STEP_BOUND + 1e-5  # float32 rounding of (v + d) - v
    assert torch.all((delta != 0).sum(dim=-1) <= BUDGET)
    assert torch.equal(changed, (delta != 0).sum(dim=-1))
    assert not delta[:, layout.repair_mask].any()


def test_jump_reference_reproduces_a0_external_code_rule() -> None:
    layout = Layout.create(FIXTURE_SEED)
    values = torch.randn(DESTINATIONS)
    peers = torch.stack((values, values[layout.peer1], values[layout.peer2]), 1)
    target = peers.median(dim=1).values
    expected = values + select((target - values).abs()) * (target - values)
    updated, _ = repair(values, "ext_jump", layout)
    assert torch.equal(updated, expected)


def test_external_repair_is_a_function_of_live_state_only_and_cannot_resurrect() -> None:
    layout = Layout.create(FIXTURE_SEED)
    values = torch.randn(DESTINATIONS)
    for kind in ("ext_bistable", "ext_median", "ext_jump"):
        first, _ = repair(values.clone(), kind, layout)
        second, _ = repair(values.clone(), kind, layout)
        assert torch.equal(first, second)
        zero, changed = repair(torch.zeros(DESTINATIONS), kind, layout)
        assert not zero.any() and int(changed) == 0


def test_bistable_restores_live_majority_and_cements_wrong_majority() -> None:
    layout = Layout.create(FIXTURE_SEED)
    task, labels = acquire(FIXTURE_SEED)
    values = initial_values(layout, task)
    addresses = layout.logical_to_physical[: 3 * TASK_BITS].reshape(TASK_BITS, 3)
    values[addresses[0, 0]] *= -1
    values[addresses[1, 0]] *= -1
    values[addresses[1, 1]] *= -1
    for _ in range(400):
        values, _ = repair(values, "ext_bistable", layout)
    assert torch.allclose(values[addresses[0]], task[0].expand(3))
    assert torch.allclose(values[addresses[1]], -task[1].expand(3))


def test_probe_lesion_is_recoverable_and_flips_exactly_its_count() -> None:
    layout = Layout.create(FIXTURE_SEED)
    task, labels = acquire(FIXTURE_SEED)
    values = initial_values(layout, task)
    order, replica = probe_draws(FIXTURE_SEED, 0)
    lesioned, used = perturb(values, layout, labels, order, replica)
    assert used == arms.PROBE_FRACTION_COUNT
    assert float(accuracy(lesioned, layout, labels)) == pytest.approx(1 - used / TASK_BITS)
    assert int((lesioned != values).sum()) == used
    for _ in range(400):
        lesioned, _ = repair(lesioned, "ext_bistable", layout)
    assert float(accuracy(lesioned, layout, labels)) == 1.0


def test_no_maint_row_equals_a0_damage_only_rollout() -> None:
    """Ordering: entry t of the record is the state AFTER t complete cycles.

    A0 queried each tick BEFORE that tick's fault, so retention at H here equals
    the state A0 would first query at tick H+1 (registered in protocol section 3).
    """
    result = simulate(FIXTURE_SEED, 1, [Cell(1, 1, 1)], 300, [300], trajectory_stride=1)
    layout = Layout.create(FIXTURE_SEED + arms.LAYOUT_OFFSET)
    task, labels = acquire(FIXTURE_SEED)
    state = State(initial_values(layout, task), torch.zeros(DESTINATIONS, 4))
    stream = FaultStream(FIXTURE_SEED + arms.FAULT_OFFSET)
    for tick in range(300):
        state = damage(state, stream.next())
        assert result["trajectory"][tick][0][0] == float(accuracy(state.values, layout, labels))


def test_simulation_is_deterministic_and_records_all_arms() -> None:
    cells = [Cell(1, 1, 8), Cell(2, 8, 8)]
    first = simulate(FIXTURE_SEED, 8, cells, 256, [128, 256])
    second = simulate(FIXTURE_SEED, 8, cells, 256, [128, 256])
    assert first == second
    point = first["checkpoints"]["256"]["s2_d8_e8"]
    assert set(point) == set(arms.ARMS)
    assert first["immortal_accuracy"] == 1.0
    with pytest.raises(ValueError):
        simulate(FIXTURE_SEED, 1, [Cell(1, 1, 8)], 8, [8])


def test_probe_forks_share_stream_and_bistable_closes_more_than_no_maint() -> None:
    probe = ProbeSpec(start=16, windows=(16, 256), triggers=2)
    result = simulate(FIXTURE_SEED, 32, [Cell(2, 8, 32)], 600, [600], probe)
    triggers = result["probe"]["triggers"]
    assert len(triggers) == 2
    for trig in triggers:
        b = closure(trig["parent_before"]["ext_bistable"][0], trig["fork_immediate"]["ext_bistable"][0],
                    trig["parent_after"]["ext_bistable"][256][0], trig["fork_after"]["ext_bistable"][256][0])
        n = closure(trig["parent_before"]["no_maint"][0], trig["fork_immediate"]["no_maint"][0],
                    trig["parent_after"]["no_maint"][256][0], trig["fork_after"]["no_maint"][256][0])
        assert b is not None and n is not None
        assert b > n


def test_metric_helpers() -> None:
    assert gap_recovery(0.6, 0.9, 1.0) == pytest.approx(0.75)
    assert gap_recovery(1.0, 1.0, 1.0) == 0.0
    assert closure(1.0, 0.75, 0.9, 0.9) == pytest.approx(1.0)
    assert closure(1.0, 0.75, 0.9, 0.65) == pytest.approx(0.0)
    assert closure(0.8, 0.8, 0.8, 0.8) is None
    with pytest.raises(ValueError):
        closure(0.5, 0.75, 0.5, 0.5)


def _row(seed: int, nm: float, ext: float, h: int = 2048, cell: str = "s1_d1_e1") -> dict:
    arm = lambda x: {"at_horizon": x, "whole_horizon": x, "last_quarter": x}
    return {"seed": seed, "immortal_accuracy": 1.0, "checkpoints": {str(h): {cell: {
        "no_maint": arm(nm), "ext_bistable": arm(ext), "ext_median": arm(nm), "ext_jump": arm(nm)}}}}


def test_cell_criteria_and_lexicographic_selection() -> None:
    good = [_row(s, 0.68, 0.95) for s in range(16)]
    stats = calibrate.cell_stats(good, "s1_d1_e1", 2048)
    assert stats["admissible"]
    weak = calibrate.cell_stats([_row(s, 0.68, 0.70) for s in range(16)], "s1_d1_e1", 2048)
    assert not weak["criteria"]["recovery"]
    high = calibrate.cell_stats([_row(s, 0.92, 0.99) for s in range(16)], "s1_d1_e1", 2048)
    assert not high["criteria"]["window"] and not high["criteria"]["seeds_below_gate"]
    other = dict(stats, cell="s1_d2_e1")
    later = dict(stats, horizon=4096)
    assert calibrate.choose_cell([other, later, stats]) is stats
    assert calibrate.choose_cell([weak]) is None


def test_runner_refuses_without_human_approved_freeze(tmp_path: Path) -> None:
    if (ROOT / calibrate.FREEZE).exists():
        pytest.skip("Freeze record exists; refusal path not applicable")
    with pytest.raises(RuntimeError):
        calibrate.require_freeze()


def test_harness_never_references_candidate_machinery() -> None:
    forbidden = ("propose", "training_step", "select(", "meta_", "intercept")
    for name in ("law.py", "arms.py", "calibrate.py"):
        source = (ROOT / "sub_a0_cal_v1" / name).read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, (name, token)


def test_registered_grid_constants() -> None:
    assert calibrate.HORIZONS[0] == 1024 and calibrate.HORIZONS[-1] == 65536
    assert len(calibrate.HORIZONS) == 13
    assert calibrate.SHRINK == (1, 2) and calibrate.DRIFT == (1, 2, 4, 8)
    assert calibrate.ERASE == (1, 8, 32) and calibrate.WINDOWS == (16, 64, 256, 1024)
    assert REPAIR_COEFFICIENTS == 42 and TASK_BITS == 256 and BUDGET == 256


def test_replay_refuses_without_human_approved_freeze(tmp_path: Path) -> None:
    if (ROOT / calibrate.FREEZE).exists():
        pytest.skip("Freeze record exists; refusal path not applicable")
    with pytest.raises(RuntimeError):
        calibrate.replay(tmp_path, 2000, 1)


def test_predecessor_validation_rejects_foreign_or_failed_outputs(tmp_path: Path) -> None:
    freeze = {"source_hashes": {"x": "1"}}
    (tmp_path / "manifest.json").write_text(
        '{"stage": "stage1", "kind": "A0_CAL_CONTROL_ARMS_ONLY", "source_hashes": {"x": "2"}}')
    (tmp_path / "summary.json").write_text('{"status": "SELECTED"}')
    with pytest.raises(RuntimeError):
        calibrate.load_predecessor(tmp_path, "stage1", freeze, "SELECTED")
    with pytest.raises(RuntimeError):
        calibrate.load_predecessor(tmp_path, "stage2", freeze, "SELECTED")


def _probe_row(seed: int, triggers: int, nm_at_h: float, lesions: int = 64) -> dict:
    cell = "s1_d1_e1"
    arm = {"at_horizon": nm_at_h, "whole_horizon": nm_at_h, "last_quarter": nm_at_h}
    trig = {
        "perturbed": {a: [lesions] for a in ("no_maint", "ext_bistable", "ext_median")},
        "parent_before": {a: [1.0] for a in ("no_maint", "ext_bistable", "ext_median")},
        "fork_immediate": {a: [0.75] for a in ("no_maint", "ext_bistable", "ext_median")},
        "parent_after": {a: {w: [1.0] for w in calibrate.WINDOWS} for a in ("no_maint", "ext_bistable", "ext_median")},
        "fork_after": {"no_maint": {w: [0.75] for w in calibrate.WINDOWS},
                       "ext_bistable": {w: [1.0] for w in calibrate.WINDOWS},
                       "ext_median": {w: [0.9] for w in calibrate.WINDOWS}},
    }
    return {"seed": seed, "checkpoints": {"2048": {cell: {"no_maint": arm}}},
            "probe": {"triggers": [trig] * triggers}}


def test_probe_gate_requires_identifiable_triggers_in_enough_pressured_seeds() -> None:
    good = [_probe_row(s, 4, 0.7) for s in range(16)]
    result = calibrate.probe_stats(good, 2048, "s1_d1_e1")
    assert result["selected_window"] == 16
    sparse = [_probe_row(s, 4 if s < 11 else 2, 0.7) for s in range(16)]
    assert calibrate.probe_stats(sparse, 2048, "s1_d1_e1")["selected_window"] is None
    unpressured = [_probe_row(s, 4, 0.7 if s < 11 else 0.95) for s in range(16)]
    assert calibrate.probe_stats(unpressured, 2048, "s1_d1_e1")["selected_window"] is None
    short = [_probe_row(s, 4, 0.7, lesions=63) for s in range(16)]
    assert calibrate.probe_stats(short, 2048, "s1_d1_e1")["selected_window"] is None


def test_natural_lesion_records_have_in_range_windows() -> None:
    result = simulate(FIXTURE_SEED, 32, [Cell(1, 1, 32)], 512, [512])
    assert result["natural_lesions"]
    for event in result["natural_lesions"]:
        assert all(event["tick"] + int(w) <= 512 for w in event["after"])
    summary = calibrate.natural_lesion_stats([result], 0)
    assert summary["descriptive_only"]
