"""A0-cal control arms: acquisition-only fit, external repairers and simulator.

Nothing here constructs, trains or evaluates the SUB-A0 candidate updater.
External repairers are host-computed (EXTERNAL, invulnerable) controls that read
only the current damaged live state; none stores a clean copy or reads labels.
Labels are used only by the evaluator readout and the evaluator-side probe.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import torch
from torch import Tensor
from torch.nn import functional as F

from sub_a0_v1.model import BUDGET, DESTINATIONS, REPAIR_COEFFICIENTS, TASK_BITS, Layout
from sub_a0_cal_v1.law import Cell, ParamFaultStream, apply, cell_terms

ARMS = ("no_maint", "ext_bistable", "ext_median", "ext_jump")
PROBE_ARMS = ("no_maint", "ext_bistable", "ext_median")
STEP_BOUND = 0.05  # candidate write physics: |0.05 * tanh(.)| <= 0.05
# Deterministic acquisition magnitude: Adam(lr=0.1) on BCE from zero yields the
# same |T| for every coefficient and seed. One content-blind scalar, verified by test.
BISTABLE_MAGNITUDE = 4.449178695678711
PROBE_FRACTION_COUNT = 64          # 25% of the 256 task coefficients
PROBE_REVERSAL = -2.5              # replica := -2.5 * mean(other two replicas)
NATURAL_WINDOWS = (16, 64, 256, 1024)
LAYOUT_OFFSET = 30000
FAULT_OFFSET = 50000
PROBE_OFFSET = 80000


def acquire(seed: int) -> tuple[Tensor, Tensor]:
    """Task-only acquisition, identical to step 1 of ``sub_a0_v1.run.train``."""
    gen = torch.Generator().manual_seed(seed)
    labels = torch.randint(2, (TASK_BITS,), generator=gen).float()
    with torch.enable_grad():
        task = torch.zeros(TASK_BITS, requires_grad=True)
        optimizer = torch.optim.Adam([task], lr=0.1)
        for _ in range(128):
            optimizer.zero_grad()
            F.binary_cross_entropy_with_logits(task, labels).backward()
            optimizer.step()
    return task.detach(), labels


def initial_values(layout: Layout, task: Tensor) -> Tensor:
    """Packed physical values. R is zero: no control arm reads or uses it."""
    return layout.pack(task, torch.zeros(REPAIR_COEFFICIENTS))


def accuracy(values: Tensor, layout: Layout, labels: Tensor) -> Tensor:
    """Full-table evaluator accuracy for values of shape [..., DESTINATIONS]."""
    task = values[..., layout.logical_to_physical[: 3 * TASK_BITS]]
    logits = task.reshape(*values.shape[:-1], TASK_BITS, 3).mean(dim=-1)
    return ((logits > 0) == labels.bool()).float().mean(dim=-1)


def repair(values: Tensor, kind: str, layout: Layout) -> tuple[Tensor, Tensor]:
    """One budget-limited external repair step on values [..., DESTINATIONS].

    Returns new values and the count of actually changed destinations per row.
    """
    peers = torch.stack((values, values[..., layout.peer1], values[..., layout.peer2]), dim=-1)
    median = peers.median(dim=-1).values
    if kind == "ext_bistable":
        target = torch.where(median == 0, values, torch.sign(median) * BISTABLE_MAGNITUDE)
    elif kind in ("ext_median", "ext_jump"):
        target = median
    else:
        raise ValueError(f"Not an external repair arm: {kind}")
    difference = target - values
    score = difference.abs()
    if kind != "ext_jump":
        score = score.masked_fill(layout.repair_mask, float("-inf"))
    chosen = torch.argsort(score, dim=-1, descending=True, stable=True)[..., :BUDGET]
    mask = torch.zeros_like(values).scatter(-1, chosen, 1.0)
    delta = difference if kind == "ext_jump" else difference.clamp(-STEP_BOUND, STEP_BOUND)
    updated = values + mask * delta
    return updated, (updated != values).sum(dim=-1)


def probe_draws(seed: int, trigger: int) -> tuple[Tensor, Tensor]:
    gen = torch.Generator().manual_seed(PROBE_OFFSET + 100 * seed + trigger)
    order = torch.randperm(TASK_BITS, generator=gen)
    replica = torch.randint(3, (TASK_BITS,), generator=gen)
    return order, replica


def perturb(values: Tensor, layout: Layout, labels: Tensor, order: Tensor,
            replica: Tensor) -> tuple[Tensor, int]:
    """Evaluator-side recoverable lesion of one branch state values [DESTINATIONS].

    Eligible coefficients are currently read correctly and have BOTH untouched
    replicas of the correct sign, so a correct live majority survives. The chosen
    replica is set to -2.5 x the mean of the other two, which flips the mean readout.
    """
    addresses = layout.logical_to_physical[: 3 * TASK_BITS].reshape(TASK_BITS, 3)
    triplets = values[addresses]
    sign = 2 * labels - 1
    out = values.clone()
    used = 0
    for index in order.tolist():
        if used == PROBE_FRACTION_COUNT:
            break
        r = int(replica[index])
        others = [j for j in range(3) if j != r]
        trip = triplets[index]
        if not (trip.mean() * sign[index] > 0):
            continue
        if not all(float(trip[j]) * float(sign[index]) > 0 for j in others):
            continue
        out[addresses[index, r]] = PROBE_REVERSAL * trip[others].mean()
        used += 1
    return out, used


@dataclass
class ProbeSpec:
    start: int                       # earliest trigger tick (exclusive)
    windows: tuple[int, ...]         # W values
    triggers: int = 4


@dataclass
class Trigger:
    tick: int
    kind: str
    perturbed: dict[str, list[int]] = field(default_factory=dict)
    parent_before: dict[str, list[float]] = field(default_factory=dict)
    fork_immediate: dict[str, list[float]] = field(default_factory=dict)
    parent_after: dict[str, dict[int, list[float]]] = field(default_factory=dict)
    fork_after: dict[str, dict[int, list[float]]] = field(default_factory=dict)


@torch.no_grad()
def simulate(seed: int, erase: int, cells: list[Cell], horizon: int,
             checkpoints: list[int], probe: ProbeSpec | None = None,
             trajectory_stride: int = 16, deadline_check=None) -> dict[str, object]:
    """Run all control arms for one seed and one erase multiplier.

    ``cells`` must share ``erase``; they share one fault stream (identical draws),
    differing only in shrink/drift multipliers.
    """
    if any(c.erase != erase for c in cells):
        raise ValueError("Cells in one stream must share the erase multiplier")
    layout = Layout.create(seed + LAYOUT_OFFSET)
    task, labels = acquire(seed)
    start = initial_values(layout, task)
    immortal = float(accuracy(start, layout, labels))
    n_parent = len(ARMS)
    forks = 0 if probe is None else probe.triggers * len(PROBE_ARMS)
    values = start.repeat(len(cells), n_parent + forks, 1)
    rows_by_kind = {
        kind: [ARMS.index(kind)] + (
            [] if probe is None else
            [n_parent + k * len(PROBE_ARMS) + PROBE_ARMS.index(kind)
             for k in range(probe.triggers)] if kind in PROBE_ARMS else []
        )
        for kind in ARMS[1:]
    }
    stream = ParamFaultStream(seed + FAULT_OFFSET, erase)
    wanted = sorted({h for h in checkpoints} | {h - h // 4 for h in checkpoints})
    cumulative = torch.zeros(len(cells), n_parent, dtype=torch.float64)
    at: dict[int, list[list[float]]] = {}
    sums: dict[int, list[list[float]]] = {}
    trajectory: list[list[list[float]]] = []
    changed_totals = {kind: 0 for kind in ARMS[1:]}
    events = {"erase": 0, "entered_high": 0}
    natural: list[dict[str, object]] = []  # secondary natural-lesion windows
    natural_pending: dict[int, list[tuple[dict[str, object], int]]] = {}
    triggers: list[Trigger] = []
    pending: dict[int, list[tuple[Trigger, int, int]]] = {}
    last = max(horizon, 0)
    if probe is not None:
        last = horizon + max(probe.windows)
    for tick in range(1, last + 1):
        if deadline_check is not None and tick % 1024 == 0:
            deadline_check()
        raw = stream.next()
        events["erase"] += int(raw.erase_event and tick <= horizon)
        events["entered_high"] += int(bool(raw.entered_high.any()) and tick <= horizon)
        shrink, drift = cell_terms(raw, cells)
        values = apply(values, shrink, drift, raw.erase)
        for kind, rows in rows_by_kind.items():
            updated, changed = repair(values[:, rows], kind, layout)
            values[:, rows] = updated
            if tick <= horizon:
                changed_totals[kind] += int(changed[:, 0].sum())
        acc = accuracy(values, layout, labels)
        if tick <= horizon:
            cumulative += acc[:, :n_parent].double()
            if tick in wanted:
                sums[tick] = cumulative.tolist()
            if tick in checkpoints:
                at[tick] = acc[:, :n_parent].tolist()
            if tick % trajectory_stride == 0:
                trajectory.append(acc[:, :n_parent].tolist())
            if raw.erase_event:
                record = {"tick": tick, "at_event": acc[:, :n_parent].tolist(), "after": {}}
                natural.append(record)
                for window in NATURAL_WINDOWS:
                    if tick + window <= last:
                        natural_pending.setdefault(tick + window, []).append((record, window))
        for record, window in natural_pending.pop(tick, []):
            record["after"][str(window)] = acc[:, :n_parent].tolist()
        if probe is not None:
            for trig, window, k in pending.pop(tick, []):
                for kind in PROBE_ARMS:
                    parent = ARMS.index(kind)
                    fork = n_parent + k * len(PROBE_ARMS) + PROBE_ARMS.index(kind)
                    trig.parent_after.setdefault(kind, {})[window] = acc[:, parent].tolist()
                    trig.fork_after.setdefault(kind, {})[window] = acc[:, fork].tolist()
            event = bool(raw.entered_high.any()) or raw.erase_event
            if (event and tick > probe.start and len(triggers) < probe.triggers
                    and tick <= horizon):
                k = len(triggers)
                trig = Trigger(tick, "erase" if raw.erase_event else "entered_high")
                order, replica = probe_draws(seed, k)
                for kind in PROBE_ARMS:
                    parent = ARMS.index(kind)
                    fork = n_parent + k * len(PROBE_ARMS) + PROBE_ARMS.index(kind)
                    used: list[int] = []
                    for c in range(len(cells)):
                        lesioned, count = perturb(values[c, parent], layout, labels, order, replica)
                        values[c, fork] = lesioned
                        used.append(count)
                    trig.perturbed[kind] = used
                    trig.parent_before[kind] = acc[:, parent].tolist()
                    trig.fork_immediate[kind] = accuracy(values[:, fork], layout, labels).tolist()
                triggers.append(trig)
                for window in probe.windows:
                    pending.setdefault(tick + window, []).append((trig, window, k))
    results: dict[str, object] = {
        "seed": seed, "erase": erase, "horizon": horizon,
        "cells": [c.key() for c in cells], "arms": list(ARMS),
        "immortal_accuracy": immortal,
        "acquisition_accuracy": float(((task > 0) == labels.bool()).float().mean()),
        "task_abs_values": sorted({float(x) for x in task.abs()}),
        "checkpoints": {}, "events_within_horizon": events, "natural_lesions": natural,
        "changed_destinations_within_horizon": changed_totals,
        "trajectory_stride": trajectory_stride,
    }
    for h in checkpoints:
        q = h - h // 4
        results["checkpoints"][str(h)] = {
            cell.key(): {
                arm: {
                    "at_horizon": at[h][c][a],
                    "whole_horizon": sums[h][c][a] / h,
                    "last_quarter": (sums[h][c][a] - sums[q][c][a]) / (h - q),
                }
                for a, arm in enumerate(ARMS)
            }
            for c, cell in enumerate(cells)
        }
    results["trajectory"] = trajectory
    if probe is not None:
        results["probe"] = {
            "start": probe.start, "windows": list(probe.windows),
            "planned_triggers": probe.triggers, "observed_triggers": len(triggers),
            "triggers": [t.__dict__ for t in triggers],
        }
    return results


def closure(parent_before: float, fork_immediate: float, parent_after: float,
            fork_after: float) -> float | None:
    """Fraction of an injected deficit repaired, net of ongoing damage.

    1 - (parent_after - fork_after) / (parent_before - fork_immediate).
    None if the injected deficit is zero (unidentifiable trigger).
    """
    deficit = parent_before - fork_immediate
    if deficit < 0:
        raise ValueError("Negative injected deficit: probe implementation failure")
    if deficit == 0:
        return None
    return 1 - (parent_after - fork_after) / deficit


def gap_recovery(no_maint: float, repaired: float, immortal: float) -> float:
    """(repaired - no_maint) / (immortal - no_maint); 0 when there is no gap."""
    gap = immortal - no_maint
    if gap <= 0:
        return 0.0
    return (repaired - no_maint) / gap


__all__ = [
    "ARMS", "PROBE_ARMS", "BISTABLE_MAGNITUDE", "STEP_BOUND", "DESTINATIONS",
    "ProbeSpec", "acquire", "accuracy", "closure", "gap_recovery", "initial_values",
    "perturb", "probe_draws", "repair", "simulate",
]
