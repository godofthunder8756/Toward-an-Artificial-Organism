from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch import Tensor
from torch.nn import functional as F

from sub_a0_v1.metrics import allocation
from sub_a0_v1.model import (
    BUDGET, DESTINATIONS, HIDDEN, REPAIR_COEFFICIENTS, TASK_BITS, Layout,
    State, ensure_finite, initial_state, propose, select, task_logits,
    training_step, write,
)
from sub_a0_v1.world import FaultStream, damage

ROOT = Path(__file__).resolve().parents[1]
ARMS = ("sham", "pressure", "no_write", "intercept_r", "uniform", "fixed",
        "threshold", "external_code", "immortal")
HORIZON = 1024
MACS_PER_PROPOSAL = DESTINATIONS * (3 * HIDDEN + HIDDEN * HIDDEN + HIDDEN * 2)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, data: object) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, allow_nan=False)
        handle.write("\n")


def check_deadline(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise TimeoutError("Engineering command deadline exhausted")


def peak_working_set() -> int | None:
    if sys.platform != "win32":
        return None

    class Counters(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    psapi = ctypes.windll.psapi
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
    if not psapi.GetProcessMemoryInfo(
        kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb
    ):
        raise OSError("Cannot measure owned process working set")
    return int(counters.PeakWorkingSetSize)


def train(seed: int, deadline: float) -> tuple[Tensor, Tensor, Tensor, dict[str, object]]:
    started = time.monotonic()
    gen = torch.Generator().manual_seed(seed)
    labels = torch.randint(2, (TASK_BITS,), generator=gen).float()
    task = torch.zeros(TASK_BITS, requires_grad=True)
    repair = (0.1 * torch.randn(REPAIR_COEFFICIENTS, generator=gen)).requires_grad_()
    optimizer = torch.optim.Adam([task], lr=0.1)
    for _ in range(128):
        check_deadline(deadline)
        optimizer.zero_grad()
        F.binary_cross_entropy_with_logits(task, labels).backward()
        optimizer.step()
    task = task.detach()
    optimizer = torch.optim.Adam([repair], lr=0.01)
    layout = Layout.create(seed + 30000)
    losses: list[float] = []
    for iteration in range(128):
        check_deadline(deadline)
        optimizer.zero_grad()
        state = initial_state(layout, task, repair)
        faults = FaultStream(40000 + seed * 1000 + iteration)
        for _ in range(16):
            state = training_step(damage(state, faults.next()), layout)
        ensure_finite(state)
        loss = F.binary_cross_entropy_with_logits(task_logits(state, layout), labels)
        if not torch.isfinite(loss):
            raise RuntimeError("Nonfinite task-only development loss")
        loss.backward()
        if repair.grad is None or not torch.isfinite(repair.grad).all():
            raise RuntimeError("Invalid updater task-gradient")
        optimizer.step()
        losses.append(float(loss.detach()))
    return task, repair.detach(), labels, {
        "seed": seed, "acquisition_updates": 128, "meta_updates": 128,
        "development_ticks": 2048, "development_backward_calls": 256,
        "development_forward_linear_macs": 2048 * MACS_PER_PROPOSAL,
        "meta_task_losses": losses, "wall_seconds": time.monotonic() - started,
        "acquisition_accuracy": float(((task > 0) == labels.bool()).float().mean()),
    }


def probe(state: State, layout: Layout, labels: Tensor, replica: int) -> dict[str, float]:
    before = float(((task_logits(state, layout) > 0) == labels.bool()).float().mean())
    values = state.values.clone()
    positions = layout.logical_to_physical[:3 * TASK_BITS].reshape(-1, 3)[:, replica]
    values[positions] = 0
    fork = State(values, state.hidden.clone())
    immediate = float(((task_logits(fork, layout) > 0) == labels.bool()).float().mean())
    for _ in range(16):
        proposal = propose(fork, layout)
        fork, _ = write(fork, proposal, select(proposal.score))
        ensure_finite(fork)
    after = float(((task_logits(fork, layout) > 0) == labels.bool()).float().mean())
    return {"before": before, "immediate": immediate, "after": after, "gain": after - immediate}


@torch.no_grad()
def evaluate(
    seed: int, task: Tensor, repair: Tensor, labels: Tensor, arm: str,
    deadline: float, trace_path: Path | None = None,
) -> tuple[dict[str, object], str]:
    if arm not in ARMS:
        raise ValueError("Unknown engineering arm")
    layout = Layout.create(seed + 30000)
    state = initial_state(layout, task, repair)
    faults = FaultStream(50000 + seed)
    queries = torch.randint(16, (HORIZON,), generator=torch.Generator().manual_seed(seed + 60000))
    uniform_gen = torch.Generator().manual_seed(seed + 70000)
    wr = wt = attempts = 0
    correct_counts: list[int] = []
    capacities: list[dict[str, object]] = []
    trace_hash = hashlib.sha256()
    handle = None if trace_path is None else trace_path.open("x", encoding="utf-8")
    try:
        for tick in range(HORIZON):
            check_deadline(deadline)
            query = int(queries[tick])
            prediction = task_logits(state, layout).reshape(16, 16)[query] > 0
            correct = int((prediction == labels.reshape(16, 16)[query].bool()).sum())
            correct_counts.append(correct)
            fault = faults.next()
            if arm not in ("sham", "immortal"):
                state = damage(state, fault)
            proposal = propose(state, layout)
            mask = select(proposal.score)
            if arm == "uniform":
                mask = select(torch.rand(DESTINATIONS, generator=uniform_gen))
            elif arm == "fixed":
                mask = torch.zeros(DESTINATIONS)
                mask[(torch.arange(BUDGET) + tick * BUDGET) % DESTINATIONS] = 1
            elif arm == "threshold":
                disagreement = (
                    state.values - state.values[layout.peer1]
                ).abs() + (state.values - state.values[layout.peer2]).abs()
                mask = select(disagreement) * (disagreement > 0.1)
            elif arm == "external_code":
                peer_values = torch.stack(
                    (state.values, state.values[layout.peer1], state.values[layout.peer2]), 1
                )
                target = peer_values.median(dim=1).values
                proposal = type(proposal)(target - state.values, (target - state.values).abs(), proposal.hidden)
                mask = select(proposal.score)
            attempts += int(mask.sum())
            intercept = layout.repair_mask if arm == "intercept_r" else None
            if arm == "no_write":
                intercept = torch.ones(DESTINATIONS, dtype=torch.bool)
            state, changed = write(state, proposal, mask, intercept=intercept)
            ensure_finite(state)
            r_writes = int((changed & layout.repair_mask).sum())
            t_writes = int((changed & ~layout.repair_mask).sum())
            wr += r_writes
            wt += t_writes
            logical = layout.logical(state.values)
            row = {
                "tick": tick + 1, "query": query, "prediction": prediction.int().tolist(),
                "correct": correct, "writes_r": r_writes, "writes_t": t_writes,
                "attempts": int(mask.sum()),
                "changed_abs_sum": float((mask * proposal.delta).abs()[changed].sum()),
                "task_abs_mean": float(logical[:TASK_BITS].abs().mean()),
                "repair_abs_mean": float(logical[TASK_BITS:].abs().mean()),
            }
            encoded = json.dumps(row, sort_keys=True, allow_nan=False) + "\n"
            trace_hash.update(encoded.encode())
            if handle is not None:
                handle.write(encoded)
            if tick + 1 in (256, 512, 768) and arm in ("pressure", "intercept_r"):
                capacities.append({"tick": tick + 1, **probe(state, layout, labels, (tick + 1) // 256 - 1)})
    finally:
        if handle is not None:
            handle.close()
    metrics = allocation(wr, wt, 3 * REPAIR_COEFFICIENTS, 3 * TASK_BITS, HORIZON)
    metrics.update({
        "arm": arm, "seed": seed, "accuracy": sum(correct_counts) / (16 * HORIZON),
        "last_quarter_accuracy": sum(correct_counts[-256:]) / (16 * 256),
        "write_attempts": attempts, "capacity_probes": capacities,
        "proposal_calls": HORIZON,
        "linear_forward_macs": HORIZON * MACS_PER_PROPOSAL,
        "probe_linear_forward_macs": len(capacities) * 16 * MACS_PER_PROPOSAL,
    })
    return metrics, trace_hash.hexdigest()


@torch.no_grad()
def deletion_control(seed: int) -> dict[str, object]:
    layout = Layout.create(seed + 30000)
    state = State(torch.zeros(DESTINATIONS), torch.zeros(DESTINATIONS, HIDDEN))
    for _ in range(16):
        proposal = propose(state, layout)
        state, _ = write(state, proposal, select(proposal.score))
    if state.values.any() or state.hidden.any():
        raise RuntimeError("Zero information unexpectedly reconstructed")
    return {"zero_state_remains_zero": True, "original_table_available": False}


def manifest() -> dict[str, object]:
    boundary = json.loads((ROOT / "SUB_A0_BOUNDARY_FREEZE_v1.json").read_text())
    registration = json.loads((ROOT / "SUB_A0_ALLOCATION_REGISTRATION_v1.json").read_text())
    for filename, expected in (
        (boundary["file"], boundary["sha256"]),
        (registration["design_file"], registration["design_sha256"]),
        (registration["prior_art_file"], registration["prior_art_sha256"]),
    ):
        if digest(ROOT / filename) != expected:
            raise RuntimeError(f"Frozen input changed: {filename}")
    paths = sorted((ROOT / "sub_a0_v1").glob("*.py"))
    paths += [ROOT / "SUB_A0_ENGINEERING_PROTOCOL_v1.md",
              ROOT / "SUB_A0_BOUNDARY_FREEZE_v1.json",
              ROOT / "SUB_A0_ALLOCATION_REGISTRATION_v1.json"]
    return {
        "kind": "ENGINEERING_ONLY", "finals_authorized": False,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_hashes": {str(p.relative_to(ROOT)): digest(p) for p in paths},
        "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__,
        "torch_threads": torch.get_num_threads(), "device": "cpu",
        "planned_seeds": [0, 1], "horizon": HORIZON, "write_budget": BUDGET,
        "stored_learned_scalars": DESTINATIONS,
        "unique_developmental_coefficients": TASK_BITS + REPAIR_COEFFICIENTS,
        "vulnerable_hidden_scalars": DESTINATIONS * HIDDEN,
        "soft_internal_deadline_seconds": 1140,
        "outer_watchdog_required_seconds": 1200,
    }


def execute(output: Path) -> None:
    started = time.monotonic()
    deadline = started + 1140
    output.mkdir(exist_ok=False)
    save_json(output / "manifest.json", manifest())
    completed: list[dict[str, object]] = []
    stop_reason = None
    for seed in (0, 1):
        task, repair, labels, development = train(seed, deadline)
        np.savez(
            output / f"acquired_{seed}.npz",
            task=task.numpy(), repair=repair.numpy(), evaluator_labels=labels.numpy(),
        )
        save_json(output / f"development_{seed}.json", development)
        arms: dict[str, dict[str, object]] = {}
        for arm in ARMS:
            metrics, trace_hash = evaluate(
                seed, task, repair, labels, arm, deadline, output / f"trace_{seed}_{arm}.jsonl"
            )
            metrics["trace_sha256"] = trace_hash
            arms[arm] = metrics
            save_json(output / f"arm_{seed}_{arm}.json", metrics)
            print(f"seed={seed} arm={arm} accuracy={metrics['accuracy']:.6f} A={metrics['A']:.6f}", flush=True)
        pressure, sham, null = arms["pressure"], arms["sham"], arms["no_write"]
        enrichment = pressure["A"] - sham["A"]
        seed_summary = {
            "seed": seed, "arms": arms, "deletion_control": deletion_control(seed),
            "allocation_D": enrichment,
            "allocation_engineering_success": pressure["A"] > 0.1 and enrichment > 0.1,
            "maintenance_effect": pressure["accuracy"] - null["accuracy"],
            "cascade_last_quarter_effect": pressure["last_quarter_accuracy"] - arms["intercept_r"]["last_quarter_accuracy"],
        }
        completed.append(seed_summary)
        save_json(output / f"seed_{seed}.json", seed_summary)
        probes = pressure["capacity_probes"] + arms["intercept_r"]["capacity_probes"]
        if seed == 0 and null["accuracy"] >= 0.98 and seed_summary["maintenance_effect"] <= 0.02:
            stop_reason = "NO_WRITE_TRIVIALLY_RETAINS_SKILL"
        elif seed == 0 and all(p["before"] == p["immediate"] for p in probes):
            stop_reason = "CAPACITY_PROBE_CEILING_UNIDENTIFIABLE"
        if stop_reason:
            break
    report = {
        "kind": "ENGINEERING_ONLY", "completed_seeds": [x["seed"] for x in completed],
        "not_run_seeds": [s for s in (0, 1) if s not in [x["seed"] for x in completed]],
        "stop_reason": stop_reason, "phase_a_licensed": False,
        "confirmatory_gate_evaluated": False,
        "seeds": completed, "wall_seconds": time.monotonic() - started,
        "peak_process_working_set_bytes": peak_working_set(),
        "physical_energy_and_memory_traffic": "UNMEASURED",
    }
    save_json(output / "results.json", report)


def replay(output: Path) -> None:
    stored = json.loads((output / "manifest.json").read_text())
    for name, expected in stored["source_hashes"].items():
        if digest(ROOT / name) != expected:
            raise RuntimeError(f"Source provenance mismatch: {name}")
    report = json.loads((output / "results.json").read_text())
    replayed = 0
    for seed in report["completed_seeds"]:
        with np.load(output / f"acquired_{seed}.npz", allow_pickle=False) as archive:
            task, repair, labels = (torch.from_numpy(archive[k].copy()) for k in
                                    ("task", "repair", "evaluator_labels"))
        for arm in ARMS:
            metrics, trace_hash = evaluate(seed, task, repair, labels, arm, time.monotonic() + 120)
            expected = json.loads((output / f"arm_{seed}_{arm}.json").read_text())
            if trace_hash != expected["trace_sha256"]:
                raise RuntimeError(f"Trace replay mismatch: {seed}/{arm}")
            if any(metrics[k] != expected[k] for k in metrics):
                raise RuntimeError(f"Metric replay mismatch: {seed}/{arm}")
            replayed += 1
    save_json(output / "replay.json", {
        "passed": True, "arm_replays": replayed, "retrained": False,
        "external_replication": False, "fresh_instances": True,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("run", "replay"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    if args.operation == "run":
        execute(args.output)
    else:
        replay(args.output)


if __name__ == "__main__":
    main()
