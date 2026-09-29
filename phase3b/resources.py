"""Whole-arm accounting; distinguish counted linear MACs from other work."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
import os
import tracemalloc
from time import perf_counter
from typing import TYPE_CHECKING

import psutil  # type: ignore[import-untyped]
import torch
from torch import nn
from torch.profiler import ProfilerActivity, profile
from torch.utils.hooks import RemovableHandle

if TYPE_CHECKING:
    from phase3b.models import Arm


PARAM_CAP = 4096
FORWARD_MAC_CAP = 80_000


@dataclass
class Meter:
    """Executed linear MACs and explicitly annotated tensor work, not FLOPs.

    Backward records both input and weight matmuls only when gradients are
    requested. Logical byte counts cover annotated kernels only: allocator,
    cache, autograd, optimizer, and unannotated torch kernels remain unknown.
    """

    forward_macs: int = 0
    backward_macs: int = 0
    tanh_elements: int = 0
    log_softmax_exp_elements: int = 0
    log_softmax_log_rows: int = 0
    indexed_elements: int = 0
    argmax_comparisons: int = 0
    categorical_draws: int = 0
    modeled_tensor_bytes: int = 0


_ACTIVE: ContextVar[Meter | None] = ContextVar("phase3b_meter", default=None)


def charge(*, tanh: torch.Tensor | None = None, log_softmax: torch.Tensor | None = None,
           indexed: torch.Tensor | None = None, argmax: torch.Tensor | None = None,
           draws: torch.Tensor | None = None) -> None:
    """Charge actual executed model operations; unannotated work is not zero."""
    meter = _ACTIVE.get()
    if meter is None:
        return
    if tanh is not None:
        meter.tanh_elements += tanh.numel()
        meter.modeled_tensor_bytes += 2 * tanh.numel() * tanh.element_size()
    if log_softmax is not None:
        meter.log_softmax_exp_elements += log_softmax.numel()
        rows = log_softmax.numel() // log_softmax.shape[-1]
        meter.log_softmax_log_rows += rows
        meter.modeled_tensor_bytes += 2 * log_softmax.numel() * log_softmax.element_size()
    if indexed is not None:
        meter.indexed_elements += indexed.numel()
        meter.modeled_tensor_bytes += 2 * indexed.numel() * indexed.element_size()
    if argmax is not None:
        meter.argmax_comparisons += (argmax.shape[-1] - 1) * (argmax.numel() // argmax.shape[-1])
        meter.modeled_tensor_bytes += argmax.numel() * argmax.element_size()
    if draws is not None:
        meter.categorical_draws += draws.numel()


def observed(meter: Meter) -> dict[str, int | str]:
    return {
        "nonlinear_tanh_elements": meter.tanh_elements,
        "nonlinear_log_softmax_exp_elements": meter.log_softmax_exp_elements,
        "nonlinear_log_softmax_log_rows": meter.log_softmax_log_rows,
        "indexing_elements": meter.indexed_elements,
        "argmax_comparisons": meter.argmax_comparisons,
        "categorical_draws": meter.categorical_draws,
        "annotated_logical_tensor_bytes_estimate": meter.modeled_tensor_bytes,
        "coverage": "annotated forward read/write elements only (views and caches may avoid transfers); "
                "excludes other arithmetic, categorical internals, backward nonlinear kernels, "
                "loss, AdamW, allocator and actual CPU/GPU memory traffic",
    }


@contextmanager
def python_peak():
    """Peak of Python-traced allocations; NOT peak torch tensor/allocator memory."""
    if tracemalloc.is_tracing():
        # Cannot reset a caller's tracing peak without destroying their data.
        result = {"python_tracemalloc_peak_bytes": None,
                  "peak_memory_limitations": "tracing already active; torch allocator not captured"}
        yield result
        return
    tracemalloc.start()
    result = {"python_tracemalloc_peak_bytes": None,
              "peak_memory_limitations": "Python-traced allocations only; torch native/CPU/GPU allocator "
                                         "and process peak RSS not measured"}
    try:
        yield result
    finally:
        result["python_tracemalloc_peak_bytes"] = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()


@contextmanager
def linear_meter(model: nn.Module, meter: Meter):
    handles: list[RemovableHandle] = []
    token = _ACTIVE.set(meter)

    def forward(module: nn.Module, args: tuple[torch.Tensor, ...], output: torch.Tensor) -> None:
        if not isinstance(module, nn.Linear):
            return
        meter.forward_macs += args[0].numel() // module.in_features * module.in_features * module.out_features

    def backward(module: nn.Module, grad_in: tuple[torch.Tensor, ...] | torch.Tensor,
                 grad_out: tuple[torch.Tensor, ...] | torch.Tensor) -> None:
        if not isinstance(module, nn.Linear) or not isinstance(grad_out, tuple) or not isinstance(grad_in, tuple):
            return
        if grad_out[0] is not None:
            g = grad_out[0]
            # W gradient always needed; input gradient only if requested.
            macs = g.numel() * module.in_features
            if grad_in[0] is not None:
                macs += g.numel() * module.in_features
            meter.backward_macs += macs

    try:
        for layer in model.modules():
            if isinstance(layer, nn.Linear):
                handles.extend((layer.register_forward_hook(forward),
                                layer.register_full_backward_hook(backward)))
        yield meter
    finally:
        for h in handles:
            h.remove()
        _ACTIVE.reset(token)


def count(model: Arm) -> dict[str, int | float | str]:
    """Dry-run identical full 12-tick episode and all four decision contexts."""
    params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    meter = Meter()
    route = model.route
    if model.name == "R4" and route is None:
        model.route = (0, 1, 2, 3)
    try:
        with torch.no_grad(), linear_meter(model, meter):
            model(torch.zeros(1, 8, dtype=torch.long), torch.zeros(1, 4, 3, dtype=torch.long))
    finally:
        model.route = route
    return {"trainable_parameters": params, "forward_macs_per_episode": meter.forward_macs,
            "parameter_bytes": sum(p.numel() * p.element_size() for p in model.parameters()),
            "recurrent_state_bytes_per_episode": (4 if model.port_arm else 3 if model.name == "R3" else 1)
            * model.width * 4,
            "word_alphabet": 8 if model.word_arm else 0,
            **observed(meter)}


def require_fit(model: Arm) -> dict[str, int | float | str]:
    costs = count(model)
    if int(costs["trainable_parameters"]) > PARAM_CAP or int(costs["forward_macs_per_episode"]) > FORWARD_MAC_CAP:
        raise ValueError(f"{model.name} violates whole-arm primary cap: {costs}; STOP")
    return costs


def grid(family: str) -> tuple[tuple[int, float], ...]:
    """Exactly three pretraining widths nearest 50/75/100% of parameter cap."""
    from phase3b.models import Arm

    feasible = [(width, count(Arm(family, width))) for width in range(1, 97)]
    feasible = [(w, cost) for w, cost in feasible
                if int(cost["trainable_parameters"]) <= PARAM_CAP
                and int(cost["forward_macs_per_episode"]) <= FORWARD_MAC_CAP]
    if len(feasible) < 3:
        raise ValueError(f"{family}: no feasible three-width grid; STOP")
    chosen: list[int] = []
    for target in (PARAM_CAP * 0.5, PARAM_CAP * 0.75, PARAM_CAP):
        w, _ = min((v for v in feasible if v[0] not in chosen),
                   key=lambda v: (abs(int(v[1]["trainable_parameters"]) - target), v[0]))
        chosen.append(w)
    return tuple((w, lr) for w in chosen for lr in (0.0003, 0.001))


def profile_dry_run(model: Arm, *, batch: int = 4, training: bool = True) -> dict[str, int | float | str]:
    """Profile a throwaway full training step or evaluation forward.

    PyTorch reports tensor allocations, not physical memory bus transfers.
    Windows peak_wset is the OS process high-water mark, not an isolated
    per-arm peak; publish both limits rather than claiming hardware traffic.
    """
    if batch < 1:
        raise ValueError("batch must be positive")
    from phase3b.models import Arm

    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(0)
        # Profile a fresh throwaway topology, never mutate trained weights.
        probe = Arm(model.name, model.width, clone=model.clone)
        if probe.name == "R4":
            probe.route = (0, 1, 2, 3)
        contexts = 3 if training else 4
        common = torch.zeros((batch, 8), dtype=torch.long)
        local = torch.zeros((batch, contexts, 3), dtype=torch.long)
        optimizer = torch.optim.AdamW(probe.parameters(), lr=0.001, weight_decay=0) if training else None
        process = psutil.Process(os.getpid())
        rss_before = process.memory_info().rss
        meter = Meter()
        started = perf_counter()
        with profile(activities=[ProfilerActivity.CPU], profile_memory=True,
                     with_flops=True) as recorded, linear_meter(probe, meter):
            trace = probe(common, local, contexts=contexts, stochastic=training)
            if training:
                if trace.action_logp is None:
                    raise AssertionError("training trace missing action probabilities")
                # Synthetic evaluator zeros are not observations or scientific
                # outcomes; the same policy-gradient shape as fit() is exercised.
                from phase3b.world import loss_units

                truth = torch.zeros((batch, 4), dtype=torch.long)
                losses = loss_units(trace.actions, truth).float() / 50
                advantage = losses.detach()
                objective = torch.stack([(advantage[:, :, i] * value).mean()
                                         for i, value in enumerate(trace.action_logp)]).mean()
                if trace.token_logp is not None:
                    objective = objective + (advantage.mean(-1) * trace.token_logp).mean()
                if optimizer is None:
                    raise AssertionError("synthetic training optimizer missing")
                optimizer.zero_grad(set_to_none=True)
                objective.backward()
                torch.nn.utils.clip_grad_norm_(probe.parameters(), 1)
                optimizer.step()
        elapsed = perf_counter() - started
        events = recorded.key_averages()
        cpu = process.memory_info()
        return {
        "mode": "unscored_synthetic_full_optimizer_step" if training else "unscored_evaluation_forward",
        "batch": batch, "contexts": contexts,
        "observed_linear_forward_macs": meter.forward_macs,
        "observed_linear_backward_macs": meter.backward_macs,
        "torch_aten_operator_calls": sum(e.count for e in events if e.key.startswith("aten::")),
        "torch_reported_operator_flops": sum(e.flops for e in events),
        "torch_positive_cpu_allocator_bytes": sum(max(0, e.cpu_memory_usage) for e in events),
        "torch_net_cpu_allocator_bytes": sum(e.cpu_memory_usage for e in events),
        "torch_operator_self_cpu_time_us": sum(e.self_cpu_time_total for e in events),
        "optimizer_state_bytes": (sum(v.numel() * v.element_size()
                                      for state in optimizer.state.values()
                                      for v in state.values() if isinstance(v, torch.Tensor))
                                  if optimizer is not None else 0),
        "process_rss_before_bytes": rss_before,
        "process_rss_after_bytes": cpu.rss,
        "process_peak_working_set_bytes": cpu.peak_wset,
        "profile_wall_seconds": elapsed,
        **observed(meter),
        "coverage": "CPU operator aggregates and OS process peak; profiler overhead included; "
                "torch allocation is NOT physical bus traffic; synthetic update omits data generator",
        }