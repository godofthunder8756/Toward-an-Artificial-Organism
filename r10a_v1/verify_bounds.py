"""Exact checker for decoder-relaxation bounds; does not assume encoder capacity."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase3b_r10_v1"))
from verify import COUNTS, DENOMINATOR, POLICIES, full_costs


def check_variant(variant: dict, orientation: str, full: list[list[int]]) -> dict:
    policies = [tuple(tuple(pair) for pair in p) for p in variant["policies"]]
    legal_s3 = [(0, 0), (1, 1)] + ([(0, 1), (1, 0)] if orientation == "unrestricted"
                                   else [(0, 1)] if orientation == "positive" else [(1, 0)])
    expected = list(product(((0, 0), (0, 1), (1, 1)),
                            ((0, 2), (2, 1), (2, 2)), legal_s3))
    if policies != expected:
        raise ValueError("unexpected restricted policy family")
    indices = [POLICIES.index(p) for p in policies]
    matrix = [[row[j] for j in indices] for row in full]
    allowed = [j for j, p in enumerate(POLICIES) if p[2] in legal_s3]
    for j in allowed:
        if not any(all(row[k] <= row[j] for row in full) for k in indices):
            raise AssertionError("dominance fails to cover relaxed specialist maps")
    selected = variant["selected"]
    if len(selected) != 8 or len(set(selected)) != 8 or any(j not in range(len(policies)) for j in selected):
        raise ValueError("invalid eight-symbol code")
    encoder = [min(range(8), key=lambda w: (row[selected[w]], w)) for row in matrix]
    if encoder != variant["encoder"]:
        raise AssertionError("incorrect minimum-risk encoder")
    upper = sum(row[selected[w]] for row, w in zip(matrix, encoder))
    if upper != variant["numerator"]:
        raise AssertionError("wrong constructive objective")
    proof = variant["certificate"]
    scale = proof["scale"]
    if type(scale) is not int or scale <= 0 or proof["objective_unit"] != 5:
        raise ValueError("invalid bound scale")
    offsets = [min(row) for row in matrix]
    if any((v - offset) % 5 for row, offset in zip(matrix, offsets) for v in row):
        raise AssertionError("incorrect integer lattice")
    reduced = [[(v - offset) // 5 for v in row] for row, offset in zip(matrix, offsets)]
    target = (upper - sum(offsets)) // 5
    if proof["offset"] != sum(offsets) or proof["target"] != target:
        raise AssertionError("incorrect normalized target")
    nodes = proof["nodes"]
    stack = [(0, (), ())]
    visited = set()
    while stack:
        index, included, excluded = stack.pop()
        if type(index) is not int or not 0 <= index < len(nodes) or index in visited:
            raise ValueError("missing, repeated or cyclic node")
        visited.add(index)
        free = [j for j in range(len(policies)) if j not in included + excluded]
        node = nodes[index]
        if len(included) > 8:
            raise ValueError("illegal cardinality")
        if node["kind"] == "branch":
            j = node["policy"]
            if j not in free or len(included) == 8:
                raise ValueError("illegal branch")
            stack.extend(((node["one"], included + (j,), excluded),
                          (node["zero"], included, excluded + (j,))))
        elif node["kind"] == "dual":
            alpha = node["alpha"]
            if len(alpha) != 81 or any(type(v) is not int for v in alpha):
                raise ValueError("invalid integer row prices")
            prices = [sum(max(0, alpha[i] - reduced[i][j] * scale) for i in range(81))
                      for j in range(len(policies))]
            lower = sum(alpha) - sum(prices[j] for j in included) - sum(
                sorted((prices[j] for j in free), reverse=True)[:8 - len(included)])
            if lower != node["lower_micro_units"] or lower <= (target - 1) * scale:
                raise AssertionError("leaf does not rule out improvement")
        elif node["kind"] == "exhausted":
            if len(included) != 8 and free:
                raise ValueError("premature exhaustion")
            value = sum(min(row[j] for j in included) for row in reduced) if included else None
            if node["value"] != value or (value is not None and value < target):
                raise AssertionError("better exhausted codebook")
        else:
            raise ValueError("unknown node kind")
    if len(visited) != len(nodes):
        raise ValueError("unreachable proof nodes")
    return {"exact": str(Fraction(upper, DENOMINATOR)), "nodes": len(nodes),
            "certified_decoder_bound": True}


def verify(document: dict) -> dict:
    if document["schema"] != 1 or document["denominator"] != DENOMINATOR:
        raise ValueError("unknown schema")
    if document["counts"] != [list(n) for n in COUNTS]:
        raise ValueError("missing beliefs")
    full = full_costs()
    return {name: check_variant(document["variants"][name], name, full)
            for name in ("positive", "negative", "unrestricted")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text(encoding="utf-8"))), indent=2))
