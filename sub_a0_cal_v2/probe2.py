"""A0-cal probe v2: deeper registered lesion, engineering depth selection, stages 2-3.

Successor to the frozen v1 harness (unchanged). The ONLY probe change is the
lesion depth k: the chosen replica is set to k x the mean of the other two
(v1: k = -2.5). k is chosen on disjoint engineering seeds by a rule fixed in
SUB_A0_CAL_PROBE_v2.md, then stage 2 (calibration seeds) and stage 3 (holdout)
run with the v1 criteria, regime selection and code paths.

    python -m sub_a0_cal_v2.probe2 engineering sub_a0_cal_results_v1/probe2_engineering --stage1 sub_a0_cal_results_v1/stage1
    python -m sub_a0_cal_v2.probe2 stage2 sub_a0_cal_results_v1/probe2_stage2 --stage1 ... --engineering ...
    python -m sub_a0_cal_v2.probe2 stage3 sub_a0_cal_results_v1/probe2_stage3 --stage1 ... --stage2 ...
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

from sub_a0_cal_v1 import arms, calibrate as v1
from sub_a0_cal_v1.arms import ProbeSpec, simulate

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "SUB_A0_CAL_PROBE_v2.md"
FREEZE = "SUB_A0_CAL_PROBE_FREEZE_v2.json"
ENGINEERING_SEEDS = tuple(range(3000, 3008))
DEPTHS = (-3.0, -4.0, -5.0, -6.0)
APPROVED_DEPTH = -4.0
WALL_CAP_SECONDS = {"engineering": 1800, "stage2": 1800, "stage3": 1800}
KIND = "A0_CAL_PROBE_V2_CONTROL_ARMS_ONLY"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    paths = sorted((ROOT / "sub_a0_cal_v2").glob("*.py")) + [ROOT / PROTOCOL]
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}


def require_freeze() -> tuple[dict[str, object], dict[str, object]]:
    """Both the unchanged v1 freeze and the v2 freeze must verify."""
    base = v1.require_freeze()
    path = ROOT / FREEZE
    if not path.exists():
        raise RuntimeError("No human-approved probe-v2 freeze record: not authorized")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not record.get("human_approved"):
        raise RuntimeError("Probe-v2 freeze record lacks human approval")
    if record.get("source_hashes") != source_hashes():
        raise RuntimeError("Probe-v2 protocol/source hashes do not match current files")
    if record.get("v1_freeze_sha256") != v1.digest(ROOT / v1.FREEZE):
        raise RuntimeError("Probe-v2 freeze was made against a different v1 freeze")
    return base, record


def _job(args: tuple) -> dict[str, object]:
    seed, erase, cells, horizon, checkpoints, probe, depth, deadline = args
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    arms.PROBE_REVERSAL = depth  # read by arms.perturb at call time

    def check() -> None:
        if time.time() >= deadline:
            raise TimeoutError("Probe-v2 stage deadline exhausted")

    started = time.time()
    result = simulate(seed, erase, cells, horizon, checkpoints, probe, deadline_check=check)
    result["probe_depth"] = depth
    result["wall_seconds"] = time.time() - started
    return result


def run_jobs(jobs: list[tuple], output: Path, stage: str) -> list[dict[str, object]]:
    deadline = time.time() + WALL_CAP_SECONDS[stage]
    jobs = [job + (deadline,) for job in jobs]
    results: list[dict[str, object]] = []
    with mp.get_context("spawn").Pool(min(v1.WORKERS, len(jobs))) as pool:
        pending = [pool.apply_async(_job, (job,)) for job in jobs]
        try:
            for handle in pending:
                result = handle.get(timeout=max(1.0, deadline - time.time() + 30))
                trajectory = np.asarray(result.pop("trajectory"), dtype=np.float32)
                name = f"job_{result['seed']}_e{result['erase']}_k{abs(result['probe_depth']):g}"
                np.savez(output / f"{name}_trajectory.npz", accuracy=trajectory)
                v1.save_json(output / f"{name}.json", result)
                results.append(result)
        except BaseException:
            pool.terminate()
            raise
    return results


def manifest(stage: str, record: dict[str, object], extra: dict[str, object]) -> dict[str, object]:
    return {
        "kind": KIND, "stage": stage, "candidate_evaluated": False,
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "v1_freeze_sha256": v1.digest(ROOT / v1.FREEZE),
        "v2_freeze_sha256": digest(ROOT / FREEZE),
        "source_hashes": record["source_hashes"],
        "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__,
        "threads_per_worker": 1, "workers": v1.WORKERS, "device": "cpu",
        "wall_cap_seconds": WALL_CAP_SECONDS[stage], **extra,
    }


def load_v2(directory: Path, stage: str, record: dict[str, object], status: str) -> tuple[dict, str]:
    stored = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if stored.get("kind") != KIND or stored.get("stage") != stage:
        raise RuntimeError(f"{directory} is not a probe-v2 {stage} output")
    if stored.get("source_hashes") != record["source_hashes"]:
        raise RuntimeError(f"{directory} was produced under different probe-v2 hashes")
    if stored.get("v2_freeze_sha256") != digest(ROOT / FREEZE):
        raise RuntimeError(f"{directory} was produced under a different probe-v2 freeze")
    summary_path = directory / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("status") != status:
        raise RuntimeError(f"{directory} status is {summary.get('status')}, not {status}")
    return summary, digest(summary_path)


def selected_regime(stage1_dir: Path, base: dict[str, object]) -> tuple[object, int, str]:
    first, first_hash = v1.load_predecessor(stage1_dir, "stage1", base, "SELECTED")
    chosen = first["selected"]
    return v1.parse_cell(chosen["cell"]), chosen["horizon"], first_hash


def depth_margin(stats: dict[str, object]) -> float | None:
    """Margin of the smallest admissible window, or None if no window is admissible."""
    window = stats["selected_window"]
    if window is None:
        return None
    medians = stats["windows"][str(window)]["medians"]
    return min(medians["ext_bistable"] - v1.PROBE_EXT_MIN, v1.PROBE_NULL_MAX - medians["no_maint"])


def choose_depth(margins: dict[float, float | None]) -> float | None:
    """Registered rule: largest margin; ties go to the depth closest to the approved -4."""
    admissible = {k: m for k, m in margins.items() if m is not None}
    if not admissible:
        return None
    return min(admissible, key=lambda k: (-admissible[k], abs(k - APPROVED_DEPTH), k))


def engineering(output: Path, stage1_dir: Path) -> None:
    base, record = require_freeze()
    cell, horizon, first_hash = selected_regime(stage1_dir, base)
    output.mkdir(parents=True, exist_ok=False)
    v1.save_json(output / "manifest.json", manifest("engineering", record, {
        "seeds": list(ENGINEERING_SEEDS), "depths": DEPTHS, "cell": cell.key(),
        "horizon": horizon, "windows": v1.WINDOWS, "stage1_summary_sha256": first_hash}))
    probe = ProbeSpec(start=horizon // 8, windows=v1.WINDOWS, triggers=v1.TRIGGERS)
    jobs = [(seed, cell.erase, [cell], horizon, [horizon], probe, depth)
            for depth in DEPTHS for seed in ENGINEERING_SEEDS]
    rows = run_jobs(jobs, output, "engineering")
    per_depth, margins = {}, {}
    for depth in DEPTHS:
        subset = sorted((r for r in rows if r["probe_depth"] == depth), key=lambda r: r["seed"])
        stats = v1.probe_stats(subset, horizon, cell.key())
        per_depth[str(depth)] = stats
        margins[depth] = depth_margin(stats)
    chosen = choose_depth(margins)
    v1.save_json(output / "summary.json", {
        "cell": cell.key(), "horizon": horizon, "per_depth": per_depth,
        "margins": {str(k): v for k, v in margins.items()}, "selected_depth": chosen,
        "status": "SELECTED" if chosen is not None else "NO_ADMISSIBLE_DEPTH_STOP_AND_REPORT",
    })


def stage2(output: Path, stage1_dir: Path, engineering_dir: Path) -> None:
    base, record = require_freeze()
    cell, horizon, first_hash = selected_regime(stage1_dir, base)
    eng, eng_hash = load_v2(engineering_dir, "engineering", record, "SELECTED")
    if eng["cell"] != cell.key() or eng["horizon"] != horizon:
        raise RuntimeError("Engineering depth selection used a different regime")
    depth = eng["selected_depth"]
    output.mkdir(parents=True, exist_ok=False)
    v1.save_json(output / "manifest.json", manifest("stage2", record, {
        "seeds": list(v1.CAL_SEEDS), "cell": cell.key(), "horizon": horizon, "depth": depth,
        "windows": v1.WINDOWS, "stage1_summary_sha256": first_hash,
        "engineering_summary_sha256": eng_hash}))
    probe = ProbeSpec(start=horizon // 8, windows=v1.WINDOWS, triggers=v1.TRIGGERS)
    jobs = [(seed, cell.erase, [cell], horizon, [horizon], probe, depth) for seed in v1.CAL_SEEDS]
    rows = sorted(run_jobs(jobs, output, "stage2"), key=lambda r: r["seed"])
    stats = v1.probe_stats(rows, horizon, cell.key())
    v1.save_json(output / "summary.json", {
        "cell": cell.key(), "horizon": horizon, "depth": depth, **stats,
        "natural_lesions": v1.natural_lesion_stats(rows, 0),
        "status": "SELECTED" if stats["selected_window"] else "PROBE_UNIDENTIFIABLE_STOP_AND_REPORT",
    })


def stage3(output: Path, stage1_dir: Path, stage2_dir: Path) -> None:
    base, record = require_freeze()
    cell, horizon, first_hash = selected_regime(stage1_dir, base)
    second, second_hash = load_v2(stage2_dir, "stage2", record, "SELECTED")
    if second["cell"] != cell.key() or second["horizon"] != horizon:
        raise RuntimeError("Probe-v2 stage 2 did not probe the stage-1 selection")
    depth, window = second["depth"], second["selected_window"]
    output.mkdir(parents=True, exist_ok=False)
    v1.save_json(output / "manifest.json", manifest("stage3", record, {
        "seeds": list(v1.HOLDOUT_SEEDS), "cell": cell.key(), "horizon": horizon, "depth": depth,
        "window": window, "stage1_summary_sha256": first_hash,
        "stage2_summary_sha256": second_hash}))
    probe = ProbeSpec(start=horizon // 8, windows=v1.WINDOWS, triggers=v1.TRIGGERS)
    jobs = [(seed, cell.erase, [cell], horizon, [horizon], probe, depth) for seed in v1.HOLDOUT_SEEDS]
    rows = sorted(run_jobs(jobs, output, "stage3"), key=lambda r: r["seed"])
    regime = v1.cell_stats(rows, cell.key(), horizon)
    probes = v1.probe_stats(rows, horizon, cell.key())
    passed = regime["admissible"] and probes["windows"][str(window)]["admissible"]
    v1.save_json(output / "summary.json", {
        "cell": cell.key(), "horizon": horizon, "depth": depth, "window": window,
        "regime": regime, "probe": probes, "natural_lesions": v1.natural_lesion_stats(rows, 0),
        "status": "HOLDOUT_PASS_AWAIT_HUMAN_REGIME_FREEZE" if passed else "HOLDOUT_FAIL_STOP_AND_REPORT",
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("engineering", "stage2", "stage3"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--stage1", type=Path, required=True)
    parser.add_argument("--engineering", type=Path)
    parser.add_argument("--stage2", type=Path)
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    if args.stage == "engineering":
        engineering(args.output, args.stage1)
    elif args.stage == "stage2":
        stage2(args.output, args.stage1, args.engineering)
    else:
        stage3(args.output, args.stage1, args.stage2)


if __name__ == "__main__":
    main()
