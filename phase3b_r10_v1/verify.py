"""Solver-free R10 certificate replay using independently derived exact risks."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path
import json


COUNTS = list(product(range(3), repeat=4))
POLICIES = list(product(*(list(product(range(n), repeat=2)) for n in (2, 3, 2))))
DENOMINATOR = 4_687_500_000


def full_costs() -> list[list[int]]:
    table = []
    for counts in COUNTS:
        belief = [Fraction((1, 1, 16)[n], (17, 2, 17)[n]) for n in counts]
        weight = prod(Fraction((17, 16, 17)[n], 50) for n in counts)
        row = []
        for policy in POLICIES:
            risk = Fraction(0)
            for consumer in range(3):
                q = belief[consumer]
                for bit in (0, 1):
                    one = q * Fraction(4 if bit else 1, 5)
                    zero = (1 - q) * Fraction(1 if bit else 4, 5)
                    action = policy[consumer][bit]
                    if consumer == 1 and action == 2:
                        risk += 9 * (one + zero)
                    else:
                        target_one = (one if consumer != 2 else
                                      one * (1 - belief[3]) + zero * belief[3])
                        risk += 50 * (target_one if action == 0 else one + zero - target_one)
            integer = weight * risk * DENOMINATOR / 150
            if integer.denominator != 1:
                raise AssertionError("population risk is not on the declared integer lattice")
            row.append(integer.numerator)
        table.append(row)
    return table


def verify(document: dict) -> dict:
    if document["schema"] != 1 or document["denominator"] != DENOMINATOR:
        raise ValueError("unknown certificate schema or denominator")
    if document["counts"] != [list(n) for n in COUNTS]:
        raise ValueError("missing or reordered positive-support beliefs")
    policies = [tuple(tuple(pair) for pair in policy) for policy in document["policies"]]
    if len(set(policies)) != len(policies) or any(p not in POLICIES for p in policies):
        raise ValueError("invalid or duplicate decoder policies")
    full = full_costs()
    indices = [POLICIES.index(p) for p in policies]
    matrix = [[row[j] for j in indices] for row in full]
    # Every omitted map has a no-worse retained replacement at EVERY belief.
    for j in range(len(POLICIES)):
        if not any(all(row[k] <= row[j] for row in full) for k in indices):
            raise AssertionError(f"uncovered decoder map {j}")
    selected = document["selected"]
    if (len(selected) != 8 or len(set(selected)) != 8
            or any(type(j) is not int or not 0 <= j < len(policies) for j in selected)):
        raise ValueError("codebook must contain eight distinct valid policies")
    encoder = [min(range(8), key=lambda word: (row[selected[word]], word)) for row in matrix]
    if encoder != document["encoder"]:
        raise AssertionError("encoder is not the declared nonclairvoyant risk minimizer")
    upper = sum(row[selected[word]] for row, word in zip(matrix, encoder))
    if upper != document["numerator"]:
        raise AssertionError("incorrect feasible objective")
    certificate = document["certificate"]
    scale, unit = certificate["scale"], certificate["objective_unit"]
    if type(scale) is not int or scale <= 0 or unit != 5:
        raise ValueError("invalid certificate scale or lattice")
    offsets = [min(row) for row in matrix]
    reduced = [[(v - offset) // unit for v in row] for row, offset in zip(matrix, offsets)]
    if any((v - offset) % unit for row, offset in zip(matrix, offsets) for v in row):
        raise AssertionError("wrong objective lattice")
    target = (upper - sum(offsets)) // unit
    if certificate["offset"] != sum(offsets) or certificate["target"] != target:
        raise AssertionError("wrong normalized target")
    nodes = certificate["nodes"]
    visited: set[int] = set()
    stack = [(0, (), ())]
    leaves = 0
    while stack:
        index, included, excluded = stack.pop()
        if type(index) is not int or not 0 <= index < len(nodes) or index in visited:
            raise ValueError("missing, repeated or cyclic certificate node")
        visited.add(index)
        if len(included) > 8:
            raise ValueError("invalid branch cardinality")
        node = nodes[index]
        free = [j for j in range(len(policies)) if j not in included + excluded]
        if node["kind"] == "branch":
            j = node["policy"]
            if type(j) is not int or j not in free or len(included) == 8:
                raise ValueError("invalid binary partition")
            stack.extend(((node["one"], included + (j,), excluded),
                          (node["zero"], included, excluded + (j,))))
        elif node["kind"] == "dual":
            alpha = node["alpha"]
            if len(alpha) != 81 or any(type(v) is not int for v in alpha):
                raise ValueError("invalid exact dual proposal")
            prices = [sum(max(0, alpha[i] - reduced[i][j] * scale) for i in range(81))
                      for j in range(len(policies))]
            lower = (sum(alpha) - sum(prices[j] for j in included)
                     - sum(sorted((prices[j] for j in free), reverse=True)[:8 - len(included)]))
            if lower != node["lower_micro_units"] or lower <= (target - 1) * scale:
                raise AssertionError("leaf does not exclude a strictly better integer code")
            leaves += 1
        elif node["kind"] == "exhausted":
            if len(included) != 8 and free:
                raise ValueError("premature exhaustion")
            available = included if len(included) == 8 else included + tuple(free)
            value = sum(min(row[j] for j in available) for row in reduced) if available else None
            if value != node["value"] or (value is not None and value < target):
                raise AssertionError("exhausted node contains a better code")
            leaves += 1
        else:
            raise ValueError("unknown certificate node")
    if len(visited) != len(nodes):
        raise ValueError("unreachable certificate nodes")
    floor = Fraction(sum(min(row) for row in full), DENOMINATOR)
    optimum = Fraction(upper, DENOMINATOR)
    return {"certified": True, "full_decoder_maps": len(POLICIES),
            "retained_decoder_maps": len(policies), "positive_support_beliefs": 81,
            "nodes": len(nodes), "leaves": leaves,
            "r10_exact": str(optimum), "r10_loss": float(optimum),
            "full_information_exact": str(floor), "full_information_loss": float(floor),
            "capacity_excess_exact": str(optimum - floor),
            "capacity_excess": float(optimum - floor)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text(encoding="utf-8"))),
                     indent=2, sort_keys=True))
