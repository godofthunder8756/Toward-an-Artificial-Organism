from __future__ import annotations

import inspect

import pytest
import torch

from sub_a0_v1.metrics import allocation
from sub_a0_v1.model import (
    BUDGET, DESTINATIONS, HIDDEN, REPAIR_COEFFICIENTS, TASK_BITS,
    Layout, Proposal, State, ensure_finite, initial_state, propose, select,
    task_logits, training_step, write,
)
from sub_a0_v1.run import deletion_control
from sub_a0_v1.world import Fault, FaultStream, damage


def fixture() -> tuple[Layout, State]:
    torch.manual_seed(7)
    layout = Layout.create(19)
    task = torch.randn(TASK_BITS)
    repair = torch.randn(REPAIR_COEFFICIENTS) * 0.1
    return layout, initial_state(layout, task, repair)


def test_layout_is_complete_disjoint_and_peer_consistent() -> None:
    layout, state = fixture()
    assert torch.equal(layout.logical_to_physical.sort().values, torch.arange(DESTINATIONS))
    assert int(layout.repair_mask.sum()) == 3 * REPAIR_COEFFICIENTS
    assert torch.equal(state.values, state.values[layout.peer1])
    assert torch.equal(state.values, state.values[layout.peer2])
    assert not torch.equal(Layout.create(20).logical_to_physical, layout.logical_to_physical)


def test_every_performing_coefficient_participates_in_live_proposal() -> None:
    layout, _ = fixture()
    task = torch.randn(TASK_BITS)
    repair = (torch.randn(REPAIR_COEFFICIENTS) * 0.1).requires_grad_()
    state = initial_state(layout, task, repair)
    state = State(state.values, torch.randn(DESTINATIONS, HIDDEN))
    proposal = propose(state, layout)
    (proposal.delta.sum() + proposal.score.sum()).backward()
    assert repair.grad is not None
    assert torch.all(repair.grad != 0)


def test_performing_damage_changes_values_not_just_permission() -> None:
    layout, state = fixture()
    original = propose(state, layout)
    damaged = state.values.clone()
    damaged[layout.repair_mask] = 0
    changed = propose(State(damaged, state.hidden), layout)
    assert not torch.equal(original.delta, changed.delta)
    assert not torch.equal(original.score, changed.score)


def test_updater_can_write_every_own_coefficient() -> None:
    layout, state = fixture()
    proposal = Proposal(torch.ones(DESTINATIONS), torch.zeros(DESTINATIONS), state.hidden)
    updated, changed = write(state, proposal, torch.ones(DESTINATIONS))
    assert changed[layout.repair_mask].all()
    assert torch.allclose(updated.values, state.values + 1)


def test_interception_drops_r_writes_without_disabling_t() -> None:
    layout, state = fixture()
    proposal = Proposal(torch.ones(DESTINATIONS), torch.zeros(DESTINATIONS), state.hidden)
    updated, changed = write(
        state, proposal, torch.ones(DESTINATIONS), intercept=layout.repair_mask
    )
    assert not changed[layout.repair_mask].any()
    assert changed[~layout.repair_mask].all()
    assert torch.equal(updated.values[layout.repair_mask], state.values[layout.repair_mask])


def test_tie_rule_is_lowest_physical_index_and_budget_is_uniform() -> None:
    mask = select(torch.zeros(DESTINATIONS))
    assert int(mask.sum()) == BUDGET
    assert mask[:BUDGET].all() and not mask[BUDGET:].any()


def test_write_counts_ignore_zero_updates() -> None:
    _, state = fixture()
    proposal = Proposal(torch.zeros(DESTINATIONS), torch.zeros(DESTINATIONS), state.hidden)
    _, changed = write(state, proposal, select(proposal.score))
    assert not changed.any()


def test_proposer_receives_no_labels_faults_clean_weights_or_bank_inputs() -> None:
    assert tuple(inspect.signature(propose).parameters) == ("state", "layout")
    _, state = fixture()
    assert set(vars(state)) == {"values", "hidden"}


def test_shrink_drift_erasure_cover_r_t_and_persistent_hidden_state() -> None:
    layout, state = fixture()
    fault = Fault(
        torch.ones(DESTINATIONS), torch.ones(DESTINATIONS),
        torch.zeros(DESTINATIONS, dtype=torch.bool), torch.ones(DESTINATIONS, HIDDEN),
    )
    out = damage(state, fault)
    assert (out.values[layout.repair_mask] == 1).all()
    assert (out.values[~layout.repair_mask] == 1).all()
    assert (out.hidden == 1).all()
    erased = damage(out, Fault(
        fault.shrink, fault.drift, torch.ones(DESTINATIONS, dtype=torch.bool), fault.hidden_drift
    ))
    assert not erased.values.any() and not erased.hidden.any()


def test_fault_stream_replays_independently_of_policy() -> None:
    first, second = FaultStream(9), FaultStream(9)
    for _ in range(20):
        a, b = first.next(), second.next()
        for name in ("shrink", "drift", "erase", "hidden_drift"):
            assert torch.equal(getattr(a, name), getattr(b, name))


def test_training_forward_is_the_deployed_hard_write_graph() -> None:
    layout, state = fixture()
    trained_forward = training_step(state, layout)
    proposal = propose(state, layout)
    deployed, _ = write(state, proposal, select(proposal.score))
    torch.testing.assert_close(trained_forward.values, deployed.values, rtol=0, atol=0)


def test_task_readout_depends_only_on_live_task_storage() -> None:
    layout, state = fixture()
    logits = task_logits(state, layout)
    values = state.values.clone()
    values[layout.repair_mask] += 100
    assert torch.equal(task_logits(State(values, state.hidden), layout), logits)


@pytest.mark.parametrize("nr,nt", [(300, 100), (30, 10), (126, 768)])
def test_opportunity_normalization_removes_bank_size(nr: int, nt: int) -> None:
    assert allocation(nr, nt, nr, nt, 10)["A"] == 0


def test_no_allocation_is_flagged_failure() -> None:
    result = allocation(0, 0, 3, 9, 10)
    assert result["A"] == 0 and result["flag"] == "NO_ALLOCATION"


@pytest.mark.parametrize("args", [(1, 1, 0, 3, 10), (1, 1, 3, 0, 10),
                                 (1, 1, 3, 3, 0), (31, 1, 3, 3, 10)])
def test_invalid_metrics_are_explicit(args: tuple[int, ...]) -> None:
    with pytest.raises(ValueError):
        allocation(*args)


def test_complete_information_deletion_cannot_regenerate_table() -> None:
    assert deletion_control(0)["zero_state_remains_zero"]


def test_nan_state_invalidates_run() -> None:
    _, state = fixture()
    values = state.values.clone()
    values[0] = float("nan")
    with pytest.raises(RuntimeError, match="Nonfinite"):
        ensure_finite(State(values, state.hidden))
