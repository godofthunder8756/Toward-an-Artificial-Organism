"""Post-final R10 population coding oracle; never trains a neural model."""

from __future__ import annotations

from itertools import product
from math import comb, prod
from pathlib import Path
import argparse
import hashlib
import json
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp, linprog
from scipy.sparse import coo_matrix


COUNTS = tuple(product(range(3), repeat=4))
TRUTHS = tuple(product(range(2), repeat=4))
DENOMINATOR = 16 * 25**4 * 5 * 150
DUAL_SCALE = 1_000_000
OBJECTIVE_UNIT = 5


def component_costs() -> tuple[list[tuple[int, int]], ...]:
    return tuple(list(product(range(size), repeat=2)) for size in (2, 3, 2))


def costs() -> tuple[np.ndarray, list[tuple[tuple[int, int], ...]]]:
    """Integer population joint risks, including each legal local reading."""
    maps = component_costs()
    components = []
    for consumer, policies in enumerate(maps):
        table = np.zeros((81, len(policies)), dtype=np.int64)
        for row, counts in enumerate(COUNTS):
            for truth in TRUTHS:
                common_mass = prod(
                    comb(2, n) * 4 ** (n if z else 2 - n)
                    for n, z in zip(counts, truth)
                )
                target = truth[consumer] if consumer < 2 else truth[2] ^ truth[3]
                for bit in (0, 1):
                    mass = common_mass * (4 if bit == truth[consumer] else 1)
                    for col, policy in enumerate(policies):
                        action = policy[bit]
                        loss = 9 if consumer == 1 and action == 2 else 50 * (action != target)
                        table[row, col] += mass * loss
        # Component-wise pointwise dominance safely eliminates decoder maps.
        keep = [j for j in range(len(policies)) if not any(
            np.all(table[:, k] <= table[:, j]) and np.any(table[:, k] < table[:, j])
            for k in range(len(policies)) if k != j
        )]
        components.append((table[:, keep], [policies[j] for j in keep]))
    policies = list(product(*(entry[1] for entry in components)))
    matrix = np.stack([
        sum(components[i][0][:, components[i][1].index(policy[i])] for i in range(3))
        for policy in policies
    ], axis=1)
    return matrix, policies


def facility_problem(matrix: np.ndarray):
    """Choose at most eight policies and assign every belief to one of them."""
    rows, cols = matrix.shape
    variables = cols + rows * cols
    rr, cc, vv = [], [], []
    for row in range(rows):
        for col in range(cols):
            x = cols + row * cols + col
            rr.extend((row, rows + row * cols + col, rows + row * cols + col))
            cc.extend((x, x, col))
            vv.extend((1, 1, -1))
    rr.extend([rows + rows * cols] * cols)
    cc.extend(range(cols))
    vv.extend([1] * cols)
    a = coo_matrix((vv, (rr, cc)), shape=(rows + rows * cols + 1, variables)).tocsc()
    lower = np.concatenate((np.ones(rows), np.full(rows * cols, -np.inf), [-np.inf]))
    upper = np.concatenate((np.ones(rows), np.zeros(rows * cols), [8]))
    objective = np.concatenate((np.zeros(cols), matrix.ravel() / DENOMINATOR))
    return objective, a, lower, upper, cols


def exact_lower(matrix: np.ndarray, alpha: list[int], included: list[int],
                excluded: list[int]) -> int:
    """Exact Lagrangian bound in micro-units; valid for ANY supplied alpha."""
    prices = np.maximum(0, np.asarray(alpha, dtype=np.int64)[:, None]
                        - matrix * DUAL_SCALE).sum(axis=0)
    free = [j for j in range(matrix.shape[1]) if j not in included + excluded]
    remaining = 8 - len(included)
    return (sum(alpha) - sum(int(prices[j]) for j in included)
            - sum(sorted((int(prices[j]) for j in free), reverse=True)[:remaining]))


def certify(matrix: np.ndarray, selected: list[int]) -> dict:
    """Branch on facilities; every bound is checked with integer arithmetic."""
    offsets = matrix.min(axis=1)
    reduced = (matrix - offsets[:, None]) // OBJECTIVE_UNIT
    if np.any((matrix - offsets[:, None]) % OBJECTIVE_UNIT):
        raise AssertionError("objective lattice changed")
    target = int(reduced[:, selected].min(axis=1).sum())
    objective, a, _, upper, cols = facility_problem(matrix - offsets[:, None])
    nodes: list[dict] = []
    stack: list[tuple[list[int], list[int], int | None, str | None]] = [([], [], None, None)]
    while stack:
        included, excluded, parent, edge = stack.pop()
        index = len(nodes)
        node: dict = {}
        nodes.append(node)
        if parent is not None:
            nodes[parent][edge] = index
        if len(included) == 8 or len(included) + len(excluded) == cols:
            available = included if len(included) == 8 else [
                j for j in range(cols) if j not in excluded
            ]
            value = int(reduced[:, available].min(axis=1).sum()) if available else None
            if value is not None and value < target:
                raise AssertionError("discovered better codebook; rerun optimization")
            node.update(kind="exhausted", value=value)
            continue
        bounds = [(0.0, 1.0)] * (cols + 81 * cols)
        for j in included:
            bounds[j] = (1.0, 1.0)
        for j in excluded:
            bounds[j] = (0.0, 0.0)
        lp = linprog(objective, A_eq=a[:81], b_eq=np.ones(81),
                     A_ub=a[81:], b_ub=upper[81:], bounds=bounds, method="highs")
        if not lp.success:
            raise RuntimeError(f"LP proposal failed at node {index}: {lp.message}")
        alpha = [round(float(v) * DENOMINATOR / OBJECTIVE_UNIT * DUAL_SCALE)
                 for v in lp.eqlin.marginals]
        lower = exact_lower(reduced, alpha, included, excluded)
        # Strictly greater than target-1 excludes every better integer objective.
        if lower > (target - 1) * DUAL_SCALE:
            node.update(kind="dual", alpha=alpha, lower_micro_units=lower)
        else:
            free = [j for j in range(cols) if j not in included + excluded]
            branch = min(free, key=lambda j: (abs(float(lp.x[j]) - 0.5), j))
            node.update(kind="branch", policy=branch)
            stack.append((included, excluded + [branch], index, "zero"))
            stack.append((included + [branch], excluded, index, "one"))
        if len(nodes) % 100 == 0:
            print("certificate nodes", len(nodes), "pending", len(stack), flush=True)
    return {"scale": DUAL_SCALE, "objective_unit": OBJECTIVE_UNIT,
            "offset": int(offsets.sum()), "target": target, "nodes": nodes}


def solve(output: Path) -> None:
    started = time.perf_counter()
    matrix, policies = costs()
    print("policies", len(policies), "denominator", DENOMINATOR, flush=True)
    objective, a, lower, upper, cols = facility_problem(matrix)
    result = milp(objective, integrality=np.concatenate((np.ones(cols), np.zeros(81 * cols))),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(a, lower, upper),
                  options={"mip_rel_gap": 0, "time_limit": 300})
    if not result.success or result.x is None:
        raise RuntimeError(f"MILP proposal failed: {result.message}")
    selected = np.flatnonzero(result.x[:cols] > 0.5).tolist()
    numerator = int(matrix[:, selected].min(axis=1).sum())
    print("feasible", numerator, numerator / DENOMINATOR, "selected", selected, flush=True)
    certificate = certify(matrix, selected)
    document = {
        "schema": 1, "scope": "EXTERNAL population oracle; no neural training",
        "denominator": DENOMINATOR, "numerator": numerator,
        "counts": COUNTS, "policies": policies, "selected": selected,
        "encoder": matrix[:, selected].argmin(axis=1).tolist(),
        "certificate": certificate,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "solver": {"message": result.message, "proposal_loss": float(result.fun)},
        "wall_seconds": time.perf_counter() - started,
    }
    with output.open("x", encoding="utf-8") as stream:
        json.dump(document, stream, sort_keys=True, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
    print("certificate complete", len(certificate["nodes"]), "nodes", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    solve(parser.parse_args().output)
