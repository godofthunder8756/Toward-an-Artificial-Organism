"""A0-cal runner: stage 1 regime grid, stage 2 probe window, stage 3 holdout.

Every stage refuses to start unless a human-approved freeze record exists whose
hashes match the protocol and this source. Control arms only: no candidate.

    python -m sub_a0_cal_v1.calibrate stage1 sub_a0_cal_results_v1/stage1
    python -m sub_a0_cal_v1.calibrate stage2 sub_a0_cal_results_v1/stage2 --stage1 ...
    python -m sub_a0_cal_v1.calibrate stage3 sub_a0_cal_results_v1/stage3 --stage1 ... --stage2 ...
    python -m sub_a0_cal_v1.calibrate replay sub_a0_cal_results_v1/stage1 --job 2000 1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import platform
import statistics
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

from sub_a0_cal_v1.arms import (
    ARMS, PROBE_FRACTION_COUNT as PROBE_LESIONS, ProbeSpec, closure, gap_recovery, simulate,
)
from sub_a0_cal_v1.law import Cell

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "SUB_A0_CAL_PROTOCOL_v1.md"
VALIDITY_GATE = "SUB_A0_VALIDITY_GATE_v1.json"
FREEZE = "SUB_A0_CAL_FREEZE_v1.json"

CAL_SEEDS = tuple(range(2000, 2016))
HOLDOUT_SEEDS = tuple(range(2100, 2116))
SHRINK = (1, 2)
DRIFT = (1, 2, 4, 8)
ERASE = (1, 8, 32)
HORIZONS = tuple(round(1024 * 2 ** (k / 2)) for k in range(13))
WINDOWS = (16, 64, 256, 1024)
TRIGGERS = 4

WINDOW_LOW, WINDOW_HIGH = 0.60, 0.75
IMMORTAL_CEILING = 0.99
RECOVERY_MIN = 0.75
GATE_INVALID = 0.90
SEEDS_BELOW_GATE_MIN = 12
PROBE_EXT_MIN = 0.75
PROBE_NULL_MAX = 0.10
PROBE_TRIGGER_MIN = 3

WALL_CAP_SECONDS = {"stage1": 5400, "stage2": 1800, "stage3": 1800}
WORKERS = 12


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    paths = sorted((ROOT / "sub_a0_cal_v1").glob("*.py"))
    paths += [ROOT / "sub_a0_v1" / "model.py", ROOT / "sub_a0_v1" / "world.py",
              ROOT / PROTOCOL, ROOT / VALIDITY_GATE]
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}


def require_freeze() -> dict[str, object]:
    path = ROOT / FREEZE
    if not path.exists():
        raise RuntimeError("No human-approved A0-cal freeze record: calibration not authorized")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not record.get("human_approved"):
        raise RuntimeError("Freeze record lacks human approval")
    if record.get("source_hashes") != source_hashes():
        raise RuntimeError("Frozen protocol/source hashes do not match current files")
    return record


def save_json(path: Path, data: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=1, allow_nan=False)
        handle.write("\n")


def grid_cells(erase: int) -> list[Cell]:
    return [Cell(s, d, erase) for s in SHRINK for d in DRIFT]


def _job(args: tuple) -> dict[str, object]:
    seed, erase, cells, horizon, checkpoints, probe, deadline = args
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

    def check() -> None:
        if time.time() >= deadline:
            raise TimeoutError("A0-cal stage deadline exhausted")

    started = time.time()
    result = simulate(seed, erase, cells, horizon, checkpoints, probe, deadline_check=check)
    result["wall_seconds"] = time.time() - started
    return result


def run_jobs(jobs: list[tuple], output: Path, stage: str) -> list[dict[str, object]]:
    deadline = time.time() + WALL_CAP_SECONDS[stage]
    jobs = [job + (deadline,) for job in jobs]
    results: list[dict[str, object]] = []
    with mp.get_context("spawn").Pool(min(WORKERS, len(jobs))) as pool:
        pending = [pool.apply_async(_job, (job,)) for job in jobs]
        try:
            for handle in pending:
                result = handle.get(timeout=max(1.0, deadline - time.time() + 30))
                trajectory = np.asarray(result.pop("trajectory"), dtype=np.float32)
                name = f"job_{result['seed']}_e{result['erase']}"
                np.savez(output / f"{name}_trajectory.npz", accuracy=trajectory)
                save_json(output / f"{name}.json", result)
                results.append(result)
        except BaseException:
            pool.terminate()
            raise
    return results


def manifest(stage: str, freeze: dict[str, object], extra: dict[str, object]) -> dict[str, object]:
    return {
        "kind": "A0_CAL_CONTROL_ARMS_ONLY", "stage": stage, "candidate_evaluated": False,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "freeze_record_sha256": digest(ROOT / FREEZE), "source_hashes": freeze["source_hashes"],
        "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__,
        "threads_per_worker": 1, "workers": WORKERS, "device": "cpu",
        "wall_cap_seconds": WALL_CAP_SECONDS[stage], **extra,
    }


def cell_stats(rows: list[dict[str, object]], cell: str, horizon: int) -> dict[str, object]:
    """Pre-registered stage-1/3 criteria for one cell at one horizon."""
    nm, ext, recov, imm = [], [], [], []
    for row in rows:
        point = row["checkpoints"][str(horizon)][cell]
        nm.append(point["no_maint"]["at_horizon"])
        ext.append(point["ext_bistable"]["at_horizon"])
        imm.append(row["immortal_accuracy"])
        recov.append(gap_recovery(nm[-1], ext[-1], imm[-1]))
    below = sum(x < GATE_INVALID for x in nm)
    stats = {
        "cell": cell, "horizon": horizon, "seeds": [r["seed"] for r in rows],
        "no_maint": nm, "ext_bistable": ext, "immortal": imm, "recovery": recov,
        "median_no_maint": statistics.median(nm),
        "median_recovery": statistics.median(recov),
        "min_immortal": min(imm), "seeds_below_gate": below,
        "references": {
            arm: statistics.median(r["checkpoints"][str(horizon)][cell][arm]["at_horizon"] for r in rows)
            for arm in ARMS
        },
    }
    stats["criteria"] = {
        "window": WINDOW_LOW <= stats["median_no_maint"] <= WINDOW_HIGH,
        "immortal_ceiling": stats["min_immortal"] >= IMMORTAL_CEILING,
        "recovery": stats["median_recovery"] >= RECOVERY_MIN,
        "seeds_below_gate": below >= SEEDS_BELOW_GATE_MIN,
    }
    stats["admissible"] = all(stats["criteria"].values())
    return stats


def selection_key(stats: dict[str, object]) -> tuple:
    cell = stats["cell"]
    s, d, e = (int(part[1:]) for part in cell.split("_"))
    departure = math.log2(s) + math.log2(d) + math.log2(e)
    return (departure, stats["horizon"], abs(stats["median_no_maint"] - 0.675), s, d, e)


def choose_cell(all_stats: list[dict[str, object]]) -> dict[str, object] | None:
    admissible = [x for x in all_stats if x["admissible"]]
    return min(admissible, key=selection_key) if admissible else None


def achievable_range(all_stats: list[dict[str, object]]) -> dict[str, object]:
    with_recovery = [x for x in all_stats if x["criteria"]["recovery"]]
    return {
        "median_no_maint_min": min(x["median_no_maint"] for x in all_stats),
        "median_no_maint_max": max(x["median_no_maint"] for x in all_stats),
        "median_no_maint_range_where_recovery_holds": (
            [min(x["median_no_maint"] for x in with_recovery),
             max(x["median_no_maint"] for x in with_recovery)] if with_recovery else None
        ),
        "max_median_recovery": max(x["median_recovery"] for x in all_stats),
    }


def _identifiable(trig: dict[str, object], arm: str, cell_index: int) -> bool:
    return trig["perturbed"][arm][cell_index] == PROBE_LESIONS


def probe_stats(rows: list[dict[str, object]], horizon: int, cell: str,
                cell_index: int = 0) -> dict[str, object]:
    """Pre-registered stage-2/3 probe criteria per window W.

    A trigger is identifiable for an arm only if exactly 64 coefficients were
    lesioned. A seed is eligible only if it has >= 3 triggers identifiable in
    every probed arm with the window observed AND it is not SEED_NO_PRESSURE.
    Ineligible seeds stay in the reported denominator and fail the count gate.
    Medians are over eligible seeds.
    """
    probed = ("no_maint", "ext_bistable", "ext_median")
    no_pressure = {
        r["seed"]: r["checkpoints"][str(horizon)][cell]["no_maint"]["at_horizon"] >= GATE_INVALID
        for r in rows
    }
    per_window: dict[str, object] = {}
    for window in WINDOWS:
        per_seed: dict[str, dict[str, object]] = {}
        for row in rows:
            closures: dict[str, list[float]] = {arm: [] for arm in probed}
            usable = 0
            for trig in row["probe"]["triggers"]:
                if not all(_identifiable(trig, arm, cell_index) for arm in probed):
                    continue
                after = {arm: {str(k): v for k, v in trig["parent_after"][arm].items()} for arm in probed}
                if not all(str(window) in after[arm] for arm in probed):
                    continue
                usable += 1
                for arm in probed:
                    fork = {str(k): v for k, v in trig["fork_after"][arm].items()}
                    value = closure(trig["parent_before"][arm][cell_index],
                                    trig["fork_immediate"][arm][cell_index],
                                    after[arm][str(window)][cell_index], fork[str(window)][cell_index])
                    if value is None:
                        raise RuntimeError("64 lesions produced no deficit: implementation failure")
                    closures[arm].append(value)
            eligible = usable >= PROBE_TRIGGER_MIN and not no_pressure[row["seed"]]
            per_seed[str(row["seed"])] = {
                "usable_triggers": usable, "seed_no_pressure": no_pressure[row["seed"]],
                "eligible": eligible,
                "mean_closure": {arm: (sum(v) / len(v) if v else None) for arm, v in closures.items()},
            }
        eligible = [x for x in per_seed.values() if x["eligible"]]
        medians = {
            arm: (statistics.median(x["mean_closure"][arm] for x in eligible) if eligible else None)
            for arm in probed
        }
        criteria = {
            "eligible_seeds": len(eligible) >= SEEDS_BELOW_GATE_MIN * len(rows) // 16,
            "ext_bistable": medians["ext_bistable"] is not None and medians["ext_bistable"] >= PROBE_EXT_MIN,
            "no_maint": medians["no_maint"] is not None and medians["no_maint"] <= PROBE_NULL_MAX,
        }
        per_window[str(window)] = {"per_seed": per_seed, "seeds_total": len(rows),
                                   "eligible_seeds": len(eligible), "medians": medians,
                                   "criteria": criteria, "admissible": all(criteria.values())}
    chosen = next((w for w in WINDOWS if per_window[str(w)]["admissible"]), None)
    return {"windows": per_window, "selected_window": chosen}


def natural_lesion_stats(rows: list[dict[str, object]], cell_index: int) -> dict[str, object]:
    """Secondary, descriptive: seed-median of mean [acc(e+W) - acc(e)] per arm.

    e is the post-cycle tick of a natural erase event within the horizon; an event
    is dropped for a window W if e+W lies beyond the simulated run.
    """
    out: dict[str, object] = {}
    for window in WINDOWS:
        per_arm: dict[str, object] = {}
        for a, arm in enumerate(ARMS):
            seed_means = []
            for row in rows:
                deltas = [ev["after"][str(window)][cell_index][a] - ev["at_event"][cell_index][a]
                          for ev in row["natural_lesions"] if str(window) in ev["after"]]
                if deltas:
                    seed_means.append(sum(deltas) / len(deltas))
            per_arm[arm] = {"seeds_with_events": len(seed_means),
                            "median_change": statistics.median(seed_means) if seed_means else None}
        out[str(window)] = per_arm
    return {"descriptive_only": True, "windows": out}


def load_predecessor(directory: Path, stage: str, freeze: dict[str, object],
                     expected_status: str) -> tuple[dict[str, object], str]:
    """Validate a predecessor stage directory against the active freeze."""
    stored = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if stored.get("stage") != stage or stored.get("kind") != "A0_CAL_CONTROL_ARMS_ONLY":
        raise RuntimeError(f"{directory} is not a {stage} output")
    if stored.get("source_hashes") != freeze["source_hashes"]:
        raise RuntimeError(f"{directory} was produced under different source/protocol hashes")
    if stored.get("freeze_record_sha256") != digest(ROOT / FREEZE):
        raise RuntimeError(f"{directory} was produced under a different freeze record")
    if stage in ("stage1", "stage2") and stored.get("seeds") != list(CAL_SEEDS):
        raise RuntimeError(f"{directory} did not use the registered calibration seeds")
    summary_path = directory / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("status") != expected_status:
        raise RuntimeError(f"{directory} status is {summary.get('status')}, not {expected_status}")
    return summary, digest(summary_path)


def parse_cell(key: str) -> Cell:
    s, d, e = (int(part[1:]) for part in key.split("_"))
    return Cell(s, d, e)


def stage1(output: Path) -> None:
    freeze = require_freeze()
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / "manifest.json", manifest("stage1", freeze, {
        "seeds": list(CAL_SEEDS), "shrink": SHRINK, "drift": DRIFT, "erase": ERASE,
        "horizons": HORIZONS}))
    started = time.time()
    jobs = [(seed, e, grid_cells(e), max(HORIZONS), list(HORIZONS), None)
            for e in ERASE for seed in CAL_SEEDS]
    rows = run_jobs(jobs, output, "stage1")
    stats = []
    subsets = {}
    for e in ERASE:
        subsets[e] = sorted((r for r in rows if r["erase"] == e), key=lambda r: r["seed"])
        for cell in grid_cells(e):
            for h in HORIZONS:
                stats.append(cell_stats(subsets[e], cell.key(), h))
    chosen = choose_cell(stats)
    natural = None
    if chosen is not None:
        cell = parse_cell(chosen["cell"])
        natural = natural_lesion_stats(subsets[cell.erase], grid_cells(cell.erase).index(cell))
    save_json(output / "summary.json", {
        "stats": stats, "selected": chosen,
        "achievable_range": achievable_range(stats),
        "selected_cell_natural_lesions": natural,
        "status": "SELECTED" if chosen else "NO_ADMISSIBLE_CELL_STOP_AND_REPORT",
        "wall_seconds": time.time() - started,
        "worker_wall_seconds_total": sum(r["wall_seconds"] for r in rows),
    })


def stage2(output: Path, stage1_dir: Path) -> None:
    freeze = require_freeze()
    first, first_hash = load_predecessor(stage1_dir, "stage1", freeze, "SELECTED")
    chosen = first["selected"]
    cell, horizon = parse_cell(chosen["cell"]), chosen["horizon"]
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / "manifest.json", manifest("stage2", freeze, {
        "seeds": list(CAL_SEEDS), "cell": cell.key(), "horizon": horizon, "windows": WINDOWS,
        "stage1_summary_sha256": first_hash}))
    probe = ProbeSpec(start=horizon // 8, windows=WINDOWS, triggers=TRIGGERS)
    jobs = [(seed, cell.erase, [cell], horizon, [horizon], probe) for seed in CAL_SEEDS]
    rows = sorted(run_jobs(jobs, output, "stage2"), key=lambda r: r["seed"])
    stats = probe_stats(rows, horizon, cell.key())
    save_json(output / "summary.json", {
        "cell": cell.key(), "horizon": horizon, **stats,
        "natural_lesions": natural_lesion_stats(rows, 0),
        "status": "SELECTED" if stats["selected_window"] else "PROBE_UNIDENTIFIABLE_STOP_AND_REPORT",
    })


def stage3(output: Path, stage1_dir: Path, stage2_dir: Path) -> None:
    freeze = require_freeze()
    first, first_hash = load_predecessor(stage1_dir, "stage1", freeze, "SELECTED")
    second, second_hash = load_predecessor(stage2_dir, "stage2", freeze, "SELECTED")
    chosen, window = first["selected"], second["selected_window"]
    if second["cell"] != chosen["cell"] or second["horizon"] != chosen["horizon"]:
        raise RuntimeError("Stage 2 did not probe the stage-1 selection")
    cell, horizon = parse_cell(chosen["cell"]), chosen["horizon"]
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / "manifest.json", manifest("stage3", freeze, {
        "seeds": list(HOLDOUT_SEEDS), "cell": cell.key(), "horizon": horizon, "window": window,
        "stage1_summary_sha256": first_hash, "stage2_summary_sha256": second_hash}))
    probe = ProbeSpec(start=horizon // 8, windows=WINDOWS, triggers=TRIGGERS)
    jobs = [(seed, cell.erase, [cell], horizon, [horizon], probe) for seed in HOLDOUT_SEEDS]
    rows = sorted(run_jobs(jobs, output, "stage3"), key=lambda r: r["seed"])
    regime = cell_stats(rows, cell.key(), horizon)
    probes = probe_stats(rows, horizon, cell.key())
    passed = regime["admissible"] and probes["windows"][str(window)]["admissible"]
    save_json(output / "summary.json", {
        "cell": cell.key(), "horizon": horizon, "window": window,
        "regime": regime, "probe": probes, "natural_lesions": natural_lesion_stats(rows, 0),
        "status": "HOLDOUT_PASS_AWAIT_HUMAN_REGIME_FREEZE" if passed else "HOLDOUT_FAIL_STOP_AND_REPORT",
    })


def replay(output: Path, seed: int, erase: int) -> bool:
    """Recompute one saved stage-1 job without writing; compare everything but wall time."""
    freeze = require_freeze()
    load_predecessor(output, "stage1", freeze, json.loads(
        (output / "summary.json").read_text(encoding="utf-8"))["status"])
    if seed not in CAL_SEEDS or erase not in ERASE:
        raise ValueError("Replay job is not part of the registered stage-1 grid")
    stored = json.loads((output / f"job_{seed}_e{erase}.json").read_text(encoding="utf-8"))
    fresh = _job((seed, erase, grid_cells(erase), max(HORIZONS), list(HORIZONS), None,
                  time.time() + 3600))
    trajectory = np.load(output / f"job_{seed}_e{erase}_trajectory.npz", allow_pickle=False)["accuracy"]
    same_traj = np.array_equal(np.asarray(fresh.pop("trajectory"), dtype=np.float32), trajectory)
    fresh.pop("wall_seconds")
    stored.pop("wall_seconds")
    return same_traj and json.loads(json.dumps(fresh)) == stored


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("stage1", "stage2", "stage3", "replay"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--stage1", type=Path)
    parser.add_argument("--stage2", type=Path)
    parser.add_argument("--job", type=int, nargs=2, metavar=("SEED", "ERASE"))
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    if args.stage == "stage1":
        stage1(args.output)
    elif args.stage == "stage2":
        stage2(args.output, args.stage1)
    elif args.stage == "stage3":
        stage3(args.output, args.stage1, args.stage2)
    else:
        print(json.dumps({"replay_identical": replay(args.output, *args.job)}))


if __name__ == "__main__":
    main()
