from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

TASK_BITS = 256
REPAIR_COEFFICIENTS = 42
HIDDEN = 4
DESTINATIONS = 3 * (TASK_BITS + REPAIR_COEFFICIENTS)
BUDGET = 256


@dataclass(frozen=True)
class Layout:
    logical_to_physical: Tensor
    peer1: Tensor
    peer2: Tensor
    repair_mask: Tensor

    @classmethod
    def create(cls, seed: int) -> Layout:
        gen = torch.Generator().manual_seed(seed)
        permutation = torch.randperm(DESTINATIONS, generator=gen)
        logical = torch.arange(DESTINATIONS).reshape(-1, 3)
        peer1 = torch.empty(DESTINATIONS, dtype=torch.long)
        peer2 = torch.empty_like(peer1)
        peer1[permutation] = permutation[logical.roll(-1, dims=1).flatten()]
        peer2[permutation] = permutation[logical.roll(-2, dims=1).flatten()]
        repair = torch.zeros(DESTINATIONS, dtype=torch.bool)
        repair[permutation[3 * TASK_BITS:]] = True
        return cls(permutation, peer1, peer2, repair)

    def pack(self, task: Tensor, repair: Tensor) -> Tensor:
        if task.shape != (TASK_BITS,) or repair.shape != (REPAIR_COEFFICIENTS,):
            raise ValueError("Wrong acquired parameter shapes")
        logical = torch.cat((task, repair)).repeat_interleave(3)
        return torch.zeros_like(logical).scatter(0, self.logical_to_physical, logical)

    def logical(self, values: Tensor) -> Tensor:
        return values[self.logical_to_physical].reshape(-1, 3)


@dataclass(frozen=True)
class State:
    values: Tensor
    hidden: Tensor

    def detached(self) -> State:
        return State(self.values.detach().clone(), self.hidden.detach().clone())


@dataclass(frozen=True)
class Proposal:
    delta: Tensor
    score: Tensor
    hidden: Tensor


def initial_state(layout: Layout, task: Tensor, repair: Tensor) -> State:
    return State(layout.pack(task, repair), torch.zeros(DESTINATIONS, HIDDEN))


def task_logits(state: State, layout: Layout) -> Tensor:
    return layout.logical(state.values)[:TASK_BITS].mean(dim=1)


def propose(state: State, layout: Layout) -> Proposal:
    parameters = layout.logical(state.values)[TASK_BITS:].mean(dim=1)
    input_weights = parameters[:12].reshape(3, HIDDEN)
    recurrent = parameters[12:28].reshape(HIDDEN, HIDDEN)
    bias = parameters[28:32]
    output_weights = parameters[32:40].reshape(HIDDEN, 2)
    output_bias = parameters[40:42]
    inputs = torch.stack(
        (state.values, state.values[layout.peer1], state.values[layout.peer2]), dim=1
    )
    hidden = torch.tanh(inputs @ input_weights + state.hidden @ recurrent + bias)
    output = hidden @ output_weights + output_bias
    return Proposal(0.05 * torch.tanh(output[:, 0]), output[:, 1], hidden)


def select(score: Tensor, budget: int = BUDGET) -> Tensor:
    if not 0 <= budget <= DESTINATIONS:
        raise ValueError("Write budget is outside destination range")
    indices = torch.argsort(score, descending=True, stable=True)[:budget]
    mask = torch.zeros_like(score)
    mask[indices] = 1
    return mask


def write(
    state: State,
    proposal: Proposal,
    mask: Tensor,
    *,
    intercept: Tensor | None = None,
) -> tuple[State, Tensor]:
    if mask.shape != state.values.shape:
        raise ValueError("Mask shape must cover destinations")
    actual_mask = mask if intercept is None else mask * (~intercept).to(mask.dtype)
    values = state.values + actual_mask * proposal.delta
    changed = values != state.values
    return State(values, proposal.hidden), changed


def training_step(state: State, layout: Layout) -> State:
    proposal = propose(state, layout)
    hard = select(proposal.score)
    soft = torch.sigmoid(proposal.score)
    straight_through = hard + (soft - soft.detach())
    updated, _ = write(state, proposal, straight_through)
    return updated


def ensure_finite(state: State) -> None:
    if not torch.isfinite(state.values).all() or not torch.isfinite(state.hidden).all():
        raise RuntimeError("Nonfinite live state: invalid engineering run")
