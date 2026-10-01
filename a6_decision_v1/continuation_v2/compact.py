"""Compact scalar-gate dominance relaxation, justified before remaining jobs."""

from __future__ import annotations

from itertools import combinations, product
import json
import time
import warnings

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

from a6_decision_v1.exact import (
    COUNTS, JOINT_DENOMINATOR, JOINT_LIMIT, POLICIES, component_costs,
)
from a6_decision_v1.preservation import write_once
from a6_decision_v1.runner import HERE
from a6_decision_v1.search import head_farkas, normalized, rational_dual, thaw
from shared4_v1.coupled_lower import Model, exact_dual, replay_dual


def relaxation(positive):
    model = Model()
    maps = (((0, 0), (0, 1), (1, 1)), ((0, 2), (2, 1), (2, 2)),
            ((0, 0), (0, 1) if positive else (1, 0), (1, 1)))
    policies = tuple(product(*maps))
    parts = component_costs()
    p = {(j, c, m, k): model.variable(integer=True)
         for j, c, m, k in product(range(3), range(4), range(8), range(3))}
    x = {(h, c, m): model.variable(integer=True)
         for h, c, m in product(range(81), range(4), range(8))}
    q = {(j, c, m, bit): model.variable()
         for j in (0, 2) for c, m, bit in product(range(4), range(8), range(2))}
    for j, c, m in product(range(3), range(4), range(8)):
        model.row([(p[j, c, m, k], 1) for k in range(3)], 1, True)
        if j in (0, 2):
            for bit in (0, 1):
                model.row([(q[j, c, m, bit], 1)] +
                          [(p[j, c, m, k], -1) for k in range(3) if maps[j][k][bit] == 1],
                          0, True)
    offset = 0
    for h, c in product(range(81), range(4)):
        n = tuple(COUNTS[h][(c + j) % 4] for j in range(4))
        row = parts[COUNTS.index(n)]
        costs = []
        for j in range(3):
            choices = []
            for pair in maps[j]:
                policy = [maps[k][0] for k in range(3)]
                policy[j] = pair
                choices.append(row[POLICIES.index(tuple(policy))][j])
            costs.append(choices)
        minima = [min(values) for values in costs]
        offset += sum(minima)
        model.row([(x[h, c, m], 1) for m in range(8)], 1, True)
        for m, j in product(range(8), range(3)):
            ys = []
            for k in range(3):
                y = model.variable(costs[j][k] - minima[j])
                ys.append((y, 1))
                model.row([(y, 1), (p[j, c, m, k], -1)], 0)
            model.row(ys + [(x[h, c, m], -1)], 0, True)
    cp, wp = tuple(combinations(range(4), 2)), tuple(combinations(range(8), 2))
    z = {(c, d, m, n): model.variable(integer=True)
         for c, d in cp for m, n in wp}
    for c, d, m, n in z:
        for h in range(81):
            model.row([(x[h, c, m], 1), (x[h, d, n], 1), (z[c, d, m, n], -1)], 1)
            model.row([(x[h, c, n], 1), (x[h, d, m], 1), (z[c, d, m, n], 1)], 2)

    def transitivity(lookup, size):
        for a, b, c in combinations(range(size), 3):
            terms = [(lookup[a, b], 1), (lookup[b, c], 1), (lookup[a, c], -1)]
            model.row(terms, 1)
            model.row([(column, -value) for column, value in terms], 0)

    for m, n in wp:
        transitivity({(c, d): z[c, d, m, n] for c, d in cp}, 4)
    for c, d in cp:
        transitivity({(m, n): z[c, d, m, n] for m, n in wp}, 8)
    for c, bit in product(range(4), range(2)):
        for m in range(7):
            model.row([(q[0, c, m, bit], 1), (q[0, c, m + 1, bit], -1)], 0)
    for j in (0, 2):
        if j == 2:
            order = {(m, n): model.variable(integer=True) for m, n in wp}
            for m, n in wp:
                for c, bit in product(range(4), range(2)):
                    model.row([(q[j, c, m, bit], 1), (q[j, c, n, bit], -1),
                               (order[m, n], -1)], 0)
                    model.row([(q[j, c, n, bit], 1), (q[j, c, m, bit], -1),
                               (order[m, n], 1)], 1)
            transitivity(order, 8)
        order = {(c, d): model.variable(integer=True) for c, d in cp}
        for c, d in cp:
            for m, bit in product(range(8), range(2)):
                model.row([(q[j, c, m, bit], 1), (q[j, d, m, bit], -1),
                           (order[c, d], -1)], 0)
                model.row([(q[j, d, m, bit], 1), (q[j, c, m, bit], -1),
                           (order[c, d], 1)], 1)
        transitivity(order, 4)
    model.row([(j, value) for j, value in enumerate(model.cost) if value],
              JOINT_LIMIT - offset)
    return model.finish(), offset, p, policies


def run(name, started, limits):
    positive = name.endswith("positive")
    model, offset, p, policies = relaxation(positive)
    bound, proof = exact_dual(model, offset)
    assert replay_dual(model, offset, proof) == bound
    report = {
        "job": name, "formulation": "compact_scalar_v2", "s3_positive": positive,
        "whole_family_gate_necessary_dominance_relaxation": True,
        "not_a_deployed_witness": True, "gate_equivalent_by_orientation_floor": True,
        "s1_word_sort_symmetry": True, "count_collapse_is_scalar_dominance_only": True,
        "s2_sharing_dropped": True, "variables": len(model.cost), "rows": len(model.rhs),
        "offset": offset, "lifted_prior_dual": proof, "cuts": [], "training": False,
    }
    remaining = lambda: limits["solver_timeout_seconds"] - (time.monotonic() - started) - 5
    a, b, scales = normalized(model)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        if remaining() <= 1:
            raise TimeoutError("compact model construction exhausted the worker")
        lp = linprog(model.cost.astype(float) / JOINT_DENOMINATOR,
                     A_ub=a[~model.equal], b_ub=b[~model.equal],
                     A_eq=a[model.equal], b_eq=b[model.equal], bounds=(0, 1),
                     method="highs-ipm",
                     options={"time_limit": min(120, remaining()), "threads": 1})
        report["lp_NOT_CERTIFICATE"] = {"status": int(lp.status), "message": lp.message}
        report["discovered_exact_dual"] = rational_dual(model, offset, lp, scales)
        write_once(HERE / (name + "_root.json"), report)
        nodes = 0
        while remaining() > 1 and nodes < limits["node_limit"]:
            a, b, _ = normalized(model)
            result = milp(
                model.cost.astype(float) / JOINT_DENOMINATOR,
                integrality=model.integer, bounds=Bounds(0, 1),
                constraints=LinearConstraint(a, np.where(model.equal, b, -np.inf), b),
                options={"time_limit": remaining(), "node_limit": limits["node_limit"] - nodes,
                         "mip_rel_gap": 0, "threads": 1, "parallel": False},
            )
            count = getattr(result, "mip_node_count", None)
            if count is not None:
                nodes += int(count)
            report["milp_NOT_CERTIFICATE"] = {
                "status": int(result.status), "message": result.message,
                "nodes_reported": count, "aggregate_nodes": nodes,
                "objective": None if result.fun is None else float(result.fun + offset / JOINT_DENOMINATOR),
                "bound": None if getattr(result, "mip_dual_bound", None) is None else
                         float(result.mip_dual_bound + offset / JOINT_DENOMINATOR),
                "incumbent_available": result.x is not None,
            }
            if result.x is None or count is None:
                break
            choices = [[max(range(3), key=lambda k: result.x[p[j, c, m, k]])
                        for c, m in product(range(4), range(8))] for j in range(3)]
            selection = [choices[0][i] * 9 + choices[1][i] * 3 + choices[2][i]
                         for i in range(32)]
            cuts = [head_farkas(policies, selection, j, True if j == 0 else positive,
                               max(0.01, remaining())) for j in (0, 2) if remaining() > 1]
            cut = next((entry for entry in cuts if entry is not None), None)
            if cut is None:
                report["incumbent_scope"] = "dominating necessary policy relaxation, not actual RNN weights"
                break
            report["cuts"].append(cut)
            if len(report["cuts"]) >= limits["cut_limit"]:
                break
            consumer = cut["consumer"]
            thaw(model)
            model.row([(p[consumer, c, m, choices[consumer][c * 8 + m]], 1)
                       for c, m in product(range(4), range(8))], 31)
            model.finish()
    report["warnings"] = [str(w.message) for w in caught]
    report["elapsed_seconds"] = time.monotonic() - started
    return report
