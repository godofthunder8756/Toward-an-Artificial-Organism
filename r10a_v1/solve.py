"""Analytic decoder-restricted bounds; NOT automatically the neural class."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase3b_r10_v1"))
from r10 import DENOMINATOR, certify, facility_problem
from verify import COUNTS, POLICIES, full_costs


def solve(output: Path) -> None:
    full = full_costs()
    variants = {}
    for orientation in ("positive", "negative", "unrestricted"):
        s3 = [(0, 0), (1, 1)] + ([(0, 1), (1, 0)] if orientation == "unrestricted"
                                  else [(0, 1)] if orientation == "positive" else [(1, 0)])
        policies = list(product(((0, 0), (0, 1), (1, 1)),
                                ((0, 2), (2, 1), (2, 2)), s3))
        indices = [POLICIES.index(p) for p in policies]
        matrix = np.array(full, dtype=np.int64)[:, indices]
        objective, a, lower, upper, cols = facility_problem(matrix)
        result = milp(objective, integrality=np.r_[np.ones(cols), np.zeros(81 * cols)],
                      bounds=Bounds(0, 1), constraints=LinearConstraint(a, lower, upper),
                      options={"mip_rel_gap": 0, "time_limit": 300})
        if not result.success or result.x is None:
            raise RuntimeError(f"{orientation}: {result.message}")
        selected = np.flatnonzero(result.x[:cols] > 0.5).tolist()
        numerator = int(matrix[:, selected].min(axis=1).sum())
        variants[orientation] = {
            "policies": policies, "selected": selected,
            "encoder": matrix[:, selected].argmin(axis=1).tolist(),
            "numerator": numerator, "certificate": certify(matrix, selected),
        }
        print(orientation, numerator, numerator / DENOMINATOR,
              [policies[j] for j in selected], flush=True)
    document = {
        "schema": 1, "scope": "context3 arbitrary encoder + deployed affine decoder bound",
        "neural_encoder_achievability": "Requires separate analytic witness; not assumed",
        "denominator": DENOMINATOR, "counts": COUNTS, "variants": variants,
        "solver_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "r10_dependencies_sha256": {
            name: hashlib.sha256((ROOT / "phase3b_r10_v1" / name).read_bytes()).hexdigest()
            for name in ("r10.py", "verify.py")
        },
    }
    with output.open("x", encoding="utf-8") as stream:
        json.dump(document, stream, sort_keys=True, separators=(",", ":"), allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    solve(parser.parse_args().output)
