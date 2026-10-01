"""Independent integer-population and literal-graph A6 verification."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from math import comb, prod
from pathlib import Path

from a6_decision_v1.preservation import write_once


def integer_components():
    maps = tuple(product(*(tuple(product(range(n), repeat=2)) for n in (2, 3, 2))))
    rows = []
    for counts in product(range(3), repeat=4):
        multiplicity = prod(comb(2, n) for n in counts)
        losses = [[[0] * n for _ in range(2)] for n in (2, 3, 2)]
        for truth in product((0, 1), repeat=4):
            mass = multiplicity * prod(4 ** (n if z else 2 - n)
                                       for n, z in zip(counts, truth))
            for j in range(3):
                target = truth[j] if j < 2 else truth[2] ^ truth[3]
                for bit in (0, 1):
                    weight = mass * (4 if bit == truth[j] else 1)
                    for action in range(len(losses[j][bit])):
                        units = 9 if j == 1 and action == 2 else 50 * (action != target)
                        losses[j][bit][action] += weight * units
        rows.append(tuple(tuple(sum(losses[j][b][policy[j][b]] for b in (0, 1))
                                for j in range(3)) for policy in maps))
    return tuple(rows)


def verify_lemmas():
    from a6_decision_v1.exact import (
        AGGREGATE_DENOMINATOR, BASELINES, JOINT_DENOMINATOR,
        JOINT_LIMIT, POLICIES, STRICT_LIMITS, component_costs, conditional_lemmas,
    )
    integer = integer_components()
    if integer != component_costs():
        raise AssertionError("posterior and truth-enumeration population disagree")
    denominator = 4 * 16 * 25**4 * 5 * 50
    assert denominator == AGGREGATE_DENOMINATOR
    assert JOINT_DENOMINATOR == 3 * denominator
    assert F(JOINT_LIMIT, JOINT_DENOMINATOR) == F(5101889, 29296875) + F(1, 100)
    assert STRICT_LIMITS == tuple(int(b * denominator) - step
                                 for b, step in zip(BASELINES, (50, 1, 50)))
    for row in integer:
        for parts in row:
            assert parts[0] % 50 == parts[2] % 50 == 0
    floor = F(0)
    for readings in product((0, 1), repeat=2):
        truth_weights = [prod(4 if b == z else 1 for b in readings)
                         for z in (0, 1)]
        floor += F(min(truth_weights), 50)
        posterior = F(truth_weights[1], sum(truth_weights))
        assert F(4, 5) >= min(posterior, 1 - posterior)
    assert floor == F(1, 5)
    proof = conditional_lemmas()
    for source, replacement in proof["s2_replacements"].items():
        # Tuple text is data, not executable Python.
        pair = tuple(int(v.strip()) for v in source.strip("()").split(","))
        a = POLICIES.index(((0, 0), pair, (0, 0)))
        b = POLICIES.index(((0, 0), tuple(replacement), (0, 0)))
        assert all(row[b][1] <= row[a][1] for row in integer)
    return {"verified": True, "independent_integer_rows": len(integer),
            "decoder_maps": len(POLICIES), "lemmas": proof,
            "scope": "conditional S1 exclusion, strict lattice, relaxed-S2 dominance"}


def certify_candidate(document):
    import torch
    from shared4_v1.shared_witness import construct, load_weights, margin_certificate
    from shared4_v1.verify_witness import evaluate
    coefficients = [{tuple(key): F(value) for key, value in row}
                    for row in document["coefficients"]]
    offsets = [tuple(F(value) for value in row) for row in document["offsets"]]
    model = load_weights(document)
    reference = construct(coefficients, offsets)
    for name, tensor in model.state_dict().items():
        if not name.startswith("heads.") and not torch.equal(tensor, reference.state_dict()[name]):
            raise ValueError("candidate does not match certified finite-gain compiler")
    encoder = margin_certificate(coefficients, offsets, model)
    head_margin = None
    for head in model.heads:
        for word, context, bit in product(range(8), range(4), (0, 1)):
            scores, errors = [], []
            for action in range(head.out_features):
                terms = [F(float(head.bias[action])),
                         F(float(head.weight[action, word])),
                         F(float(head.weight[action, 8 + context])),
                         F(float(head.weight[action, 12])) * bit]
                scores.append(sum(terms))
                errors.append(sum(abs(v) for v in terms) * F(28, 2**24 - 28))
            winner = max(range(len(scores)), key=lambda a: (scores[a], -a))
            for action in range(len(scores)):
                if action != winner:
                    margin = scores[winner] - scores[action] - errors[winner] - errors[action]
                    head_margin = margin if head_margin is None else min(head_margin, margin)
    population = evaluate(model)
    certified = (encoder["strict_exact_real_argmax_certified"]
                 and encoder["conservative_float32_argmax_certified"]
                 and head_margin is not None and head_margin > 0)
    return {"population": population, "encoder_margin": encoder,
            "head_float32_margin_lower": str(head_margin),
            "positive_margins": certified,
            "certified_gate_PASS": bool(certified and population["prospective_gate"]["pass"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.candidate:
        import torch
        torch.set_num_threads(1)
        result = certify_candidate(json.loads(args.candidate.read_text()))
    else:
        result = verify_lemmas()
    if args.output:
        write_once(args.output, result)
    print(json.dumps(result, indent=2))
