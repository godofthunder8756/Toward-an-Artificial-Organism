"""Competence-constrained discovery; numerical status is never a certificate."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path
import time
import warnings

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.sparse import coo_matrix, diags

from a6_decision_v1.exact import (
    AGGREGATE_DENOMINATOR, COUNTS, JOINT_DENOMINATOR, JOINT_LIMIT,
    POLICIES, STRICT_LIMITS, component_costs,
)
from a6_decision_v1.preservation import ROOT, write_once
from shared4_v1.coupled_lower import (
    build_relaxation, exact_dual, full_costs, replay_dual,
)


def thaw(model):
    model.cost = model.cost.tolist()
    model.integer = model.integer.tolist()
    model.rhs = model.rhs.tolist()
    model.equal = model.equal.tolist()
    return model


def relaxation(positive: bool, ordered: bool):
    full = full_costs()
    prior = json.loads((ROOT / "r10a_v1" / "decoder_bounds.json").read_text())
    model, offset, metadata = build_relaxation(True, positive, full, prior)
    thaw(model)
    policies = tuple(product(((0, 0), (0, 1), (1, 1)),
                             ((0, 2), (2, 1), (2, 2)),
                             ((0, 0), (0, 1) if positive else (1, 0), (1, 1))))
    pkeys = tuple(product(range(4), range(8), range(27)))
    p = dict(zip(pkeys, range(len(pkeys))))
    xkeys = tuple(product(range(81), range(4), range(8)))
    x = dict(zip(xkeys, range(len(p), len(p) + len(xkeys))))
    qsize = 2 * 4 * 8 * 2
    ystart = len(p) + len(x) + qsize
    ykeys = tuple(product(range(81), range(4), range(8), range(27)))
    y = dict(zip(ykeys, range(ystart, ystart + len(ykeys))))
    zstart = ystart + len(y)
    context_pairs = tuple(combinations(range(4), 2))
    word_pairs = tuple(combinations(range(8), 2))
    encoder_keys = tuple((c, d, m, n) for c, d in context_pairs
                         for m, n in word_pairs)
    z = dict(zip(encoder_keys, range(zstart, zstart + len(encoder_keys))))
    hstart = zstart + len(z)
    expected_variables = hstart + 2 * (len(word_pairs) + len(context_pairs))
    if len(model.cost) != expected_variables:
        raise ValueError("frozen-model variable layout changed; do not adapt silently")
    for column in x.values():
        model.integer[column] = 0
    parts = component_costs()
    selected = [POLICIES.index(policy) for policy in policies]
    component_rows = [[] for _ in range(3)]
    for h, c, m, k in ykeys:
        n = tuple(COUNTS[h][(c + j) % 4] for j in range(4))
        row = parts[COUNTS.index(n)][selected[k]]
        if sum(row) - min(full[COUNTS.index(n)][j] for j in selected) != model.cost[y[h, c, m, k]]:
            raise ValueError("frozen-model assignment layout/cost disagrees")
        for consumer in range(3):
            component_rows[consumer].append((y[h, c, m, k], row[consumer]))
    gate_rows = []
    for terms, limit in zip(component_rows, STRICT_LIMITS):
        gate_rows.append(len(model.rhs))
        model.row(terms, limit)
    gate_rows.append(len(model.rhs))
    model.row([(j, v) for j, v in enumerate(model.cost) if v],
              JOINT_LIMIT - offset)

    def transitivity(lookup, size):
        for a, b, c in combinations(range(size), 3):
            terms = [(lookup[a, b], 1), (lookup[b, c], 1), (lookup[a, c], -1)]
            model.row(terms, 1)
            model.row([(column, -value) for column, value in terms], 0)

    for m, n in word_pairs:
        transitivity({(c, d): z[c, d, m, n] for c, d in context_pairs}, 4)
    for c, d in context_pairs:
        transitivity({(m, n): z[c, d, m, n] for m, n in word_pairs}, 8)
    for j in range(2):
        start = hstart + j * (len(word_pairs) + len(context_pairs))
        transitivity(dict(zip(word_pairs, range(start, start + len(word_pairs)))), 8)
        start += len(word_pairs)
        transitivity(dict(zip(context_pairs, range(start, start + len(context_pairs)))), 4)

    if ordered:
        histories = tuple(product((0, 1), repeat=8))
        hx = {(h, c, m): model.variable(integer=True)
              for h in range(256) for c in range(4) for m in range(8)}
        for h in range(256):
            for c in range(4):
                model.row([(hx[h, c, m], 1) for m in range(8)], 1, True)
            for c, d, m, n in encoder_keys:
                model.row([(hx[h, c, m], 1), (hx[h, d, n], 1),
                           (z[c, d, m, n], -1)], 1)
                model.row([(hx[h, c, n], 1), (hx[h, d, m], 1),
                           (z[c, d, m, n], 1)], 2)
        for h, counts in enumerate(COUNTS):
            matches = [i for i, history in enumerate(histories)
                       if tuple(history[j] + history[j + 4] for j in range(4)) == counts]
            if len(matches) != prod(comb(2, n) for n in counts):
                raise ValueError("history/count multiplicity mismatch")
            for c, m in product(range(4), range(8)):
                model.row([(hx[i, c, m], 1) for i in matches] +
                          [(x[h, c, m], -len(matches))], 0, True)
    metadata.update({
        "count_assignments_are_mixtures": True, "ordered_histories": ordered,
        "specialist_limits": list(STRICT_LIMITS), "joint_limit": JOINT_LIMIT,
        "s2_sharing_dropped": True, "whole_family_necessary_relaxation": True,
        "transitive_ordering_cuts": True, "gate_rows": gate_rows,
    })
    return model.finish(), offset, metadata, p, policies


def normalized(model):
    scales = np.ones(len(model.rhs), dtype=np.float64)
    # Risk rows have large integer coefficients; structural rows do not.
    for row, rhs in enumerate(model.rhs):
        if abs(rhs) > 1000:
            scales[row] = JOINT_DENOMINATOR
    return diags(1 / scales) @ model.matrix, model.rhs / scales, scales


def rational_dual(model, offset, result, scales):
    if result.status != 0:
        return None
    values = np.zeros(len(model.rhs))
    values[model.equal] = result.eqlin.marginals
    values[~model.equal] = result.ineqlin.marginals
    scale = 1_000_000
    proposed = [round(float(v) * JOINT_DENOMINATOR * scale / s)
                for v, s in zip(values, scales)]
    if any(not model.equal[r] and v > 0 for r, v in enumerate(proposed)):
        raise ValueError("invalid proposed inequality-dual sign")
    original = model.root_dual
    model.root_dual = proposed
    try:
        bound, proof = exact_dual(model, offset, scale)
    finally:
        model.root_dual = original
    if replay_dual(model, offset, proof) != bound:
        raise AssertionError("exact dual replay disagreement")
    return proof


def head_farkas(policies, selection, consumer, positive, remaining):
    rows, rhs = [], []
    for c, m in product(range(4), range(8)):
        policy = policies[selection[c * 8 + m]][consumer]
        for bit in (0, 1):
            row = [0] * 13
            sign = 1 if policy[bit] == 0 else -1
            row[m] = sign
            row[8 + c] = sign
            row[12] = sign * bit
            rows.append(row)
            rhs.append(0 if policy[bit] == 0 else -1)
    rows.append([0] * 12 + ([-1] if positive else [1]))
    rhs.append(-1 if consumer == 0 else 0)
    a, b = np.asarray(rows, float), np.asarray(rhs, float)
    result = linprog(b, A_eq=np.vstack((a.T, np.ones(len(rows)))),
                     b_eq=np.r_[np.zeros(13), 1],
                     bounds=(0, None), method="highs",
                     options={"time_limit": max(0.01, remaining), "threads": 1})
    if result.status != 0 or result.fun >= -1e-8:
        return None
    multipliers = [F(float(v)).limit_denominator(1_000_000) for v in result.x]
    if any(v < 0 for v in multipliers):
        return None
    if any(sum(v * row[j] for v, row in zip(multipliers, rows)) != 0
           for j in range(13)):
        return None
    contradiction = sum(v * r for v, r in zip(multipliers, rhs))
    if contradiction >= 0:
        return None
    return {"consumer": consumer, "positive": positive, "selection": selection,
            "multipliers": [str(v) for v in multipliers],
            "contradiction": str(contradiction)}


def run_relaxation(name, started, contract):
    positive = name.endswith("positive")
    ordered = name.startswith("f2")
    model, offset, report, p, policies = relaxation(positive, ordered)
    report.update({"job": name, "offset": offset, "variables": len(model.cost),
                   "rows": len(model.rhs), "training": False, "cuts": []})
    bound, prior_proof = exact_dual(model, offset)
    if replay_dual(model, offset, prior_proof) != bound:
        raise AssertionError("lifted prior dual failed")
    report["lifted_prior_dual"] = prior_proof
    a, b, scales = normalized(model)
    remaining = lambda: contract["solver_timeout_seconds"] - (time.monotonic() - started) - 5
    if remaining() <= 0:
        raise TimeoutError("resource budget exhausted during model construction")
    lp = linprog(model.cost.astype(float) / JOINT_DENOMINATOR,
                 A_ub=a[~model.equal], b_ub=b[~model.equal],
                 A_eq=a[model.equal], b_eq=b[model.equal], bounds=(0, 1),
                 options={"time_limit": min(120, remaining()), "threads": 1})
    report["lp_NOT_CERTIFICATE"] = {"status": int(lp.status), "message": lp.message}
    report["discovered_exact_dual"] = rational_dual(model, offset, lp, scales)
    write_once(Path(__file__).with_name(name + "_root.json"), report)
    nodes = 0
    while remaining() > 1 and nodes < contract["node_limit"]:
        a, b, _ = normalized(model)
        result = milp(
            model.cost.astype(float) / JOINT_DENOMINATOR,
            integrality=model.integer, bounds=Bounds(0, 1),
            constraints=LinearConstraint(a, np.where(model.equal, b, -np.inf), b),
            options={"time_limit": remaining(), "node_limit": contract["node_limit"] - nodes,
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
        if not ordered or result.x is None or count is None:
            break
        selection = [max(range(27), key=lambda k: result.x[p[c, m, k]])
                     for c, m in product(range(4), range(8))]
        proofs = [head_farkas(policies, selection, j, True if j == 0 else positive,
                              max(0.01, remaining()))
                  for j in (0, 2) if remaining() > 1]
        cut = next((proof for proof in proofs if proof is not None), None)
        if cut is None:
            report["incumbent_scope"] = "necessary relaxation only; not a recurrent deployed witness"
            break
        report["cuts"].append(cut)
        if len(report["cuts"]) >= contract["cut_limit"]:
            break
        thaw(model)
        model.row([(p[c, m, selection[c * 8 + m]], 1)
                   for c, m in product(range(4), range(8))], 31)
        model.finish()
    report["elapsed_seconds"] = time.monotonic() - started
    return report


def fixed_heads(kind):
    import torch
    from phase3b.models import Arm
    from shared4_v1.shared_witness import install_heads
    arm = Arm("R9", 56)
    with torch.no_grad():
        if kind == "bank":
            install_heads(arm)
        else:
            book = json.loads((ROOT / "r10a_v1" / "class_certificate.json").read_text())["codebook"]
            for head in arm.heads:
                head.weight.zero_()
                head.bias.zero_()
            for j in (0, 2):
                arm.heads[j].weight[1, 12] = 2
                for w, policy in enumerate(book):
                    arm.heads[j].weight[1, w] = {
                        (0, 0): -3, (0, 1): -1, (1, 1): 1,
                    }[tuple(policy[j])]
            arm.heads[1].weight[:, 12] = torch.tensor((0, 4, 2))
            for w, policy in enumerate(book):
                arm.heads[1].weight[:, w] = torch.tensor({
                    (0, 2): (1, -4, 0), (2, 1): (-4, 0, 1),
                    (2, 2): (-4, -4, 1),
                }[tuple(policy[1])])
        for head in arm.heads:
            head.bias.copy_(-torch.arange(head.out_features) / 1024)
    return arm.requires_grad_(False).eval()


def run_constructive(name, started, contract):
    import torch
    from shared4_v1.shared_witness import (
        construct, decoder_tables, features, quadratic_coefficients, sparse_weights,
    )
    from a6_decision_v1.verify import certify_candidate
    torch.set_num_threads(1)
    arm = fixed_heads(name.split("_")[-1])
    tables = decoder_tables(arm)
    parts = component_costs()
    assignments, variables = 4 * 81 * 8, 4 * 81 * 8 + 8 * 13
    rr, cc, vv, lower, upper = [], [], [], [], []
    components = np.zeros((3, assignments), dtype=np.int64)

    def row(terms, lo, hi):
        index = len(lower)
        for col, value in terms:
            rr.append(index); cc.append(col); vv.append(float(value))
        lower.append(float(lo)); upper.append(float(hi))

    for c, h in product(range(4), range(81)):
        r = c * 81 + h
        n = tuple(COUNTS[h][(c + j) % 4] for j in range(4))
        for w in range(8):
            components[:, r * 8 + w] = parts[COUNTS.index(n)][POLICIES.index(tables[c][w])]
        row([(r * 8 + w, 1) for w in range(8)], 1, 1)
        phi = features(COUNTS[h]) + tuple(int(k == c) for k in range(4))
        for w, other in product(range(8), repeat=2):
            if w != other:
                terms = [(r * 8 + w, -16384)]
                for j, value in enumerate(phi):
                    if value:
                        terms.extend(((assignments + w * 13 + j, value),
                                      (assignments + other * 13 + j, -value)))
                row(terms, 1 - 16384, np.inf)
    for consumer in range(3):
        row([(j, int(v) / AGGREGATE_DENOMINATOR)
             for j, v in enumerate(components[consumer])], -np.inf,
            STRICT_LIMITS[consumer] / AGGREGATE_DENOMINATOR)
    costs = components.sum(axis=0)
    row([(j, int(v) / JOINT_DENOMINATOR) for j, v in enumerate(costs)],
        -np.inf, JOINT_LIMIT / JOINT_DENOMINATOR)
    matrix = coo_matrix((vv, (rr, cc)), shape=(len(lower), variables)).tocsc()
    remaining = contract["solver_timeout_seconds"] - (time.monotonic() - started) - 5
    if remaining <= 0:
        raise TimeoutError("resource budget exhausted during constructive build")
    result = milp(
        np.r_[costs / JOINT_DENOMINATOR, np.zeros(variables - assignments)],
        integrality=np.r_[np.ones(assignments), np.zeros(variables - assignments)],
        bounds=Bounds(np.r_[np.zeros(assignments), np.full(variables - assignments, -128)],
                      np.r_[np.ones(assignments), np.full(variables - assignments, 128)]),
        constraints=LinearConstraint(matrix, lower, upper),
        options={"time_limit": remaining, "node_limit": contract["node_limit"],
                 "mip_rel_gap": 0, "threads": 1, "parallel": False},
    )
    report = {
        "job": name, "scope": "fixed heads/bounded quadratic template; discovery ONLY",
        "whole_family_lower": False, "training": False,
        "status_NOT_CERTIFICATE": int(result.status), "message": result.message,
        "nodes_reported": getattr(result, "mip_node_count", None),
        "incumbent_available": result.x is not None,
    }
    if result.x is not None:
        values = [[F(round(float(v) * 10**6), 10**6) for v in row]
                  for row in result.x[assignments:].reshape(8, 13)]
        coefficients = [quadratic_coefficients(row[:9]) for row in values]
        offsets = [tuple(row[9:]) for row in values]
        candidate = construct(coefficients, offsets)
        candidate.heads.load_state_dict(arm.heads.state_dict())
        document = {
            "parameters": sparse_weights(candidate),
            "coefficients": [[[list(key), str(value)] for key, value in coeff.items()]
                             for coeff in coefficients],
            "offsets": [[str(v) for v in row] for row in offsets],
        }
        certification = certify_candidate(document)
        document["certification"] = certification
        path = Path(__file__).with_name(name + "_candidate.json")
        write_once(path, document)
        report["candidate"] = path.name
        report["candidate_certification"] = certification
    report["elapsed_seconds"] = time.monotonic() - started
    return report


def run(name, started, contract):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        report = (run_constructive(name, started, contract) if name.startswith("f3")
                  else run_relaxation(name, started, contract))
    report["warnings"] = [str(w.message) for w in caught]
    return report
