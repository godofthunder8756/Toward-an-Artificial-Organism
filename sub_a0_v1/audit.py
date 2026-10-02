from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def trace_hashes(data: bytes) -> dict[str, str]:
    return {
        "physical_sha256": hashlib.sha256(data).hexdigest(),
        "lf_normalized_sha256": hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest(),
    }


def reconstruct(rows: list[dict[str, object]], labels: np.ndarray) -> dict[str, object]:
    if len(rows) != 1024 or labels.shape != (16, 16):
        raise RuntimeError("Wrong planned trace/task coverage")
    wr = wt = correct = attempts = last = 0
    for tick, row in enumerate(rows, start=1):
        if row["tick"] != tick:
            raise RuntimeError("Noncontiguous clock or reset in trace")
        query = row["query"]
        if not isinstance(query, int) or not 0 <= query < 16:
            raise RuntimeError("Invalid query")
        prediction = np.asarray(row["prediction"])
        if prediction.shape != (16,) or not np.isin(prediction, [0, 1]).all():
            raise RuntimeError("Invalid prediction")
        observed = int((prediction == labels[query]).sum())
        if observed != row["correct"]:
            raise RuntimeError("Logged score differs from evaluator truth")
        r, t, a = row["writes_r"], row["writes_t"], row["attempts"]
        if any(not isinstance(v, int) for v in (r, t, a)):
            raise RuntimeError("Noninteger write accounting")
        if not (0 <= r <= 126 and 0 <= t <= 768 and r + t <= a <= 256):
            raise RuntimeError("Budget or destination violation")
        wr += r
        wt += t
        correct += observed
        attempts += a
        if tick > 768:
            last += observed
    dr = Fraction(wr, 126 * 1024)
    dt = Fraction(wt, 768 * 1024)
    enrichment = Fraction(0) if dr + dt == 0 else (dr - dt) / (dr + dt)
    return {
        "writes_r": wr, "writes_t": wt, "write_attempts": attempts,
        "density_r": float(dr), "density_t": float(dt),
        "opportunities_r": 126 * 1024, "opportunities_t": 768 * 1024,
        "A": float(enrichment), "A_exact": str(enrichment),
        "accuracy": correct / (16 * 1024),
        "last_quarter_accuracy": last / (16 * 256),
    }


def audit(output: Path) -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((output / "manifest.json").read_text())
    results = json.loads((output / "results.json").read_text())
    for name, expected in manifest["source_hashes"].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Source changed: {name}")
    replay = json.loads((output / "replay.json").read_text())
    if not replay["passed"] or replay["retrained"]:
        raise RuntimeError("Fresh-instance replay missing or invalid")
    arms: list[dict[str, object]] = []
    for seed_result in results["seeds"]:
        seed = seed_result["seed"]
        if seed not in (0, 1):
            raise RuntimeError("Nonengineering seed found")
        with np.load(output / f"acquired_{seed}.npz", allow_pickle=False) as archive:
            labels = archive["evaluator_labels"].reshape(16, 16)
        for arm, summary in seed_result["arms"].items():
            raw = (output / f"trace_{seed}_{arm}.jsonl").read_bytes()
            hashes = trace_hashes(raw)
            if hashes["lf_normalized_sha256"] != summary["trace_sha256"]:
                raise RuntimeError(f"Trace content corruption: {seed}/{arm}")
            rows = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
            reconstructed = reconstruct(rows, labels)
            for key, value in reconstructed.items():
                if key == "A_exact":
                    continue
                if not math.isclose(value, summary[key], rel_tol=0, abs_tol=1e-14):
                    raise RuntimeError(f"Metric mismatch: {seed}/{arm}/{key}")
            arms.append({"seed": seed, "arm": arm, **hashes, **reconstructed})
    return {
        "passed": True, "kind": "ENGINEERING_RAW_AND_SOURCE_AUDIT",
        "external_laboratory_replication": False,
        "arm_count": len(arms), "tick_count": 1024 * len(arms),
        "original_source_hashes_unchanged": True, "fresh_graph_replay_passed": True,
        "trace_hash_semantics": "Original hashes are LF-normalized; physical hashes separately recorded",
        "auditor_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "arms": arms,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = audit(args.output)
    with (args.output / "independent_audit_v1.json").open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(f"PASS: {result['arm_count']} arms, {result['tick_count']} independently reconstructed ticks")


if __name__ == "__main__":
    main()
