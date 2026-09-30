"""Bounded analytic shared-context construction; inference is an actual R9."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from math import comb, prod
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
import torch

from phase3b.models import Arm
from phase3b_r10_v1.r10 import costs, facility_problem
from r10a_v1.encoder_witness import HISTORIES, risk_polynomial


COUNTS = tuple(product(range(3), repeat=4))
NEIGHBORS = ((0, 1), (1, 2), (2, 3), (3, 0))
PAIRS = tuple(tuple(sorted((a, b))) for i, j in NEIGHBORS
              for a, b in product((i, i + 4), (j, j + 4)))
R10 = F(5101889, 29296875)
GATE = R10 + F(1, 100)


def polynomial(policy, context):
    """Rotate the read-only singleton formula, not the runtime encoder."""
    return {tuple(sorted((bit + context - 3) % 4 + 4 * (bit // 4)
                         for bit in key)): value
            for key, value in risk_polynomial(policy).items()}


def features(counts):
    return (1, *counts, *(counts[i] * counts[j] for i, j in NEIGHBORS))


def value(coeff, history):
    return sum(v * prod(history[j] for j in key) for key, v in coeff.items())


def two_symbol_proposal():
    """One exact finite-class facility MILP, not a neural/hyperparameter sweep."""
    matrix, policies = costs()
    keep = [j for j, p in enumerate(policies)
            if p[0] in ((0, 0), (0, 1), (1, 1))
            and p[1] in ((0, 2), (2, 1), (2, 2))
            and p[2] in ((0, 0), (0, 1), (1, 1))]
    matrix, policies = matrix[:, keep], [policies[j] for j in keep]
    objective, a, lower, upper, cols = facility_problem(matrix)
    upper[-1] = 2
    result = milp(objective, integrality=np.r_[np.ones(cols), np.zeros(81 * cols)],
                  bounds=Bounds(0, 1), constraints=LinearConstraint(a, lower, upper),
                  options={"time_limit": 20, "mip_rel_gap": 0})
    if result.x is None:
        raise RuntimeError("bounded two-symbol proposal has no incumbent")
    book = [policies[j] for j in np.flatnonzero(result.x[:cols] > .5)]
    if book != [((0, 1), (0, 2), (0, 0)), ((0, 1), (2, 1), (1, 1))]:
        raise AssertionError("unexpected two-symbol alphabet")
    return book, {"message": result.message, "scope": "two-symbol reduced finite class",
                  "optimal_in_finite_class": bool(result.success)}


def install_heads(arm):
    """Shared word effects, additive context effects, one own-bit slope/head."""
    with torch.no_grad():
        for head in arm.heads:
            head.weight.zero_()
            head.bias.zero_()
        arm.heads[0].weight[1, 12] = 2
        arm.heads[2].weight[1, 12] = 2
        arm.heads[1].weight[:, 12] = torch.tensor((0, 4, 2))
        for c in range(4):
            arm.heads[0].weight[1, 8 + c] = -2 * c
            arm.heads[2].weight[1, 8 + c] = -2 * c
            arm.heads[1].weight[:, 8 + c] = torch.tensor((2 * c, -2 * c, 0))
            for bit in (0, 1):
                word = 2 * c + bit
                arm.heads[0].weight[1, word] = 2 * c - 1
                arm.heads[2].weight[1, word] = 2 * c + (-3 if bit == 0 else 1)
                base = (1, -4, 0) if bit == 0 else (-4, 0, 1)
                arm.heads[1].weight[:, word] = torch.tensor(
                    (base[0] - 2 * c, base[1] + 2 * c, base[2]))


@torch.no_grad()
def decoder_tables(arm):
    return tuple(tuple(tuple(tuple(int(a) for a in arm.read(
        torch.tensor([w, w]), torch.tensor([0, 1]), c, i).argmax(-1))
                             for i in range(3)) for w in range(8))
                 for c in range(4))


def baseline_utilities(book):
    coefficients, offsets = [], []
    for w in range(8):
        c = w // 2
        coefficients.append({key: -100 * v for key, v in polynomial(book[w % 2], c).items()})
        coefficients[-1][()] = coefficients[-1].get((), F(0)) - F(w, 1000)
        offsets.append(tuple(F(0 if k == c else -1000) for k in range(4)))
    return coefficients, offsets


def quadratic_coefficients(row):
    coeff = {(): row[0]}
    for i in range(4):
        coeff[(i,)] = coeff[(i + 4,)] = row[1 + i]
    for (i, j), v in zip(NEIGHBORS, row[5:]):
        for a, b in product((i, i + 4), (j, j + 4)):
            coeff[tuple(sorted((a, b)))] = v
    return {k: v for k, v in coeff.items() if v}


def shared_utility_proposal(tables, seconds=90):
    """One bounded MILP for GLOBAL quadratic W plus additive U, fixed heads.

    Assignments are proposal variables only. They are never used at inference.
    All resulting coefficients are rationalized and independently re-evaluated.
    """
    rows = 4 * 81
    assignments, utilities = rows * 8, 8 * 13
    variables = assignments + utilities
    rr, cc, vv, lower, upper = [], [], [], [], []
    objective = np.zeros(variables)
    for c, counts in product(range(4), COUNTS):
        r = c * 81 + COUNTS.index(counts)
        multiplicity = prod(comb(2, n) for n in counts)
        history = tuple(int(n == 2) for n in counts) + tuple(int(n > 0) for n in counts)
        mass = F(multiplicity, 1)
        for n in counts:
            mass *= F(17, 50) if n != 1 else F(4, 25)
        for w in range(8):
            objective[r * 8 + w] = float(
                mass * value(polynomial(tables[c][w], c), history) / 4)
        row = len(lower)
        for w in range(8):
            rr.append(row); cc.append(r * 8 + w); vv.append(1)
        lower.append(1); upper.append(1)
        phi = features(counts) + tuple(int(k == c) for k in range(4))
        for w, other in product(range(8), repeat=2):
            if w == other:
                continue
            row = len(lower)
            rr.append(row); cc.append(r * 8 + w); vv.append(-16384)
            for j, f in enumerate(phi):
                if f:
                    rr.extend((row, row))
                    cc.extend((assignments + 13 * w + j, assignments + 13 * other + j))
                    vv.extend((f, -f))
            lower.append(F(1, 1000) - 16384); upper.append(np.inf)
    a = coo_matrix((vv, (rr, cc)), shape=(len(lower), variables)).tocsc()
    result = milp(objective, integrality=np.r_[np.ones(assignments), np.zeros(utilities)],
                  bounds=Bounds(np.r_[np.zeros(assignments), np.full(utilities, -128)],
                                np.r_[np.ones(assignments), np.full(utilities, 128)]),
                  constraints=LinearConstraint(a, np.asarray(lower, dtype=float), upper),
                  options={"time_limit": seconds, "mip_rel_gap": 0.002})
    status = {"message": result.message, "time_limit_seconds": seconds,
              "scope": "fixed affine heads, shared quadratic utilities; NOT whole R9 class",
              "incumbent_available": result.x is not None,
              "solver_bound_not_a_whole_class_lower_bound": True}
    if result.x is None:
        return None, status
    values = [[F(round(float(v) * 10**6), 10**6) for v in row]
              for row in result.x[assignments:].reshape(8, 13)]
    status["proposal_objective"] = float(result.fun)
    return ([quadratic_coefficients(row[:9]) for row in values],
            [tuple(row[9:]) for row in values]), status


def construct(coefficients, offsets):
    """Compile 8 delayed bits + 16 neighboring ANDs into 24 of 56 units."""
    arm = Arm("R9", 56)
    with torch.no_grad():
        for parameter in arm.parameters():
            parameter.zero_()
        arm.trunk.input.weight[0, 4] = 64
        arm.trunk.input.bias[0] = -32
        for delay in range(1, 8):
            arm.trunk.hidden.weight[delay, delay - 1] = 32
        for unit, pair in enumerate(PAIRS, 8):
            arm.trunk.input.bias[unit] = -64 if 7 in pair else -32
            for bit in pair:
                if bit == 7:
                    arm.trunk.input.weight[unit, 4] = 64
                else:
                    arm.trunk.hidden.weight[unit, 6 - bit] = 32
        for w, coeff in enumerate(coefficients):
            bias = coeff.get((), F(0))
            for key, v in coeff.items():
                if not key:
                    continue
                unit = 7 - key[0] if len(key) == 1 else 8 + PAIRS.index(key)
                arm.code.weight[w, unit] = float(v / 2)
                bias += v / 2
            arm.code.bias[w] = float(bias)
            arm.code.weight[w, 56:] = torch.tensor([float(v) for v in offsets[w]])
    install_heads(arm)
    arm.requires_grad_(False)
    return arm.eval()


def rational_mapping(coefficients, offsets):
    return tuple(tuple(max(range(8), key=lambda w: (
        value(coefficients[w], h) + offsets[w][c], -w))
                       for c in range(4)) for h in HISTORIES)


def margin_certificate(coefficients, offsets, arm):
    mapping = rational_mapping(coefficients, offsets)
    gaps = []
    error_bounds = []
    for h, words in zip(HISTORIES, mapping):
        for c, winner in enumerate(words):
            ideal = [value(coefficients[w], h) + offsets[w][c] for w in range(8)]
            errors = []
            for w in range(8):
                coeff = coefficients[w]
                signed_l1 = sum(abs(v / 2) for key, v in coeff.items() if key)
                # The existing gain-32 proof bounds every signed feature by 1e-26.
                feature_error = signed_l1 * F(1, 10**26)
                representation = F(0)
                bias = coeff.get((), F(0)) + sum(v / 2 for key, v in coeff.items() if key)
                representation += abs(F(float(arm.code.bias[w])) - bias)
                for key, v in coeff.items():
                    if key:
                        unit = 7 - key[0] if len(key) == 1 else 8 + PAIRS.index(key)
                        representation += abs(F(float(arm.code.weight[w, unit])) - v / 2)
                representation += abs(F(float(arm.code.weight[w, 56 + c])) - offsets[w][c])
                # Conservative sequential float32 dot-product/addition bound.
                absolute = (abs(bias) + abs(offsets[w][c]) + signed_l1 + representation)
                arithmetic = absolute * F(62, 2**24 - 62)
                errors.append(feature_error + representation + arithmetic)
            for other in range(8):
                if other != winner:
                    gap = ideal[winner] - ideal[other]
                    gaps.append(gap)
                    error_bounds.append(errors[winner] + errors[other])
    exact_real_margin = min(g - F(1, 10**26) * sum(
        abs(v) for p in coefficients for key, v in p.items() if key) for g in gaps)
    float_margin = min(g - e for g, e in zip(gaps, error_bounds))
    return {"minimum_rational_score_gap": str(min(gaps)),
            "exact_real_margin_lower_bound": str(exact_real_margin),
            "conservative_float32_margin_lower_bound": str(float_margin),
            "strict_exact_real_argmax_certified": exact_real_margin > 0,
            "conservative_float32_argmax_certified": float_margin > 0}


@torch.no_grad()
def population(arm, expected_mapping=None):
    """Exhaust all 256 histories, 16 truths and both private readings/head."""
    common = torch.tensor(HISTORIES)
    traces = [arm(common, torch.full((256, 4, 3), b, dtype=torch.long)) for b in (0, 1)]
    words = traces[0].word.tolist()
    if traces[1].word.tolist() != words:
        raise AssertionError("word depends on private bit")
    if expected_mapping is not None and words != [list(row) for row in expected_mapping]:
        raise AssertionError("rational and actual RNN encoder disagree")
    totals = [[0] * 3 for _ in range(4)]
    for h, history in enumerate(HISTORIES):
        counts = [history[j] + history[j + 4] for j in range(4)]
        for truth in product(range(2), repeat=4):
            mass = prod(4 ** (n if z else 2 - n) for n, z in zip(counts, truth))
            for c, i in product(range(4), range(3)):
                factor = (c + i) % 4
                target = truth[factor] if i < 2 else truth[factor] ^ truth[(c + 3) % 4]
                for bit in (0, 1):
                    action = int(traces[bit].actions[i][h, c])
                    loss = 9 if i == 1 and action == 2 else 50 * (action != target)
                    totals[c][i] += mass * (4 if bit == truth[factor] else 1) * loss
    specialists = [[F(v, 16 * 25**4 * 5 * 50) for v in row] for row in totals]
    joint = [sum(row) / 3 for row in specialists]
    aggregate = [sum(row[i] for row in specialists) / 4 for i in range(3)]
    return {"context_joint_exact": [str(v) for v in joint],
            "context_specialists_exact": [[str(v) for v in row] for row in specialists],
            "population_joint_exact": str(sum(joint) / 4),
            "population_joint": float(sum(joint) / 4),
            "specialists_exact": [str(v) for v in aggregate],
            "specialists": [float(v) for v in aggregate],
            "mapping": words}


def sparse_weights(arm):
    return [{"name": name, "shape": list(t.shape),
             "nonzero": [index + [float(t[tuple(index)])]
                         for index in torch.nonzero(t, as_tuple=False).tolist()]}
            for name, t in arm.named_parameters()]


def load_weights(document):
    arm = Arm("R9", 56)
    parameters = dict(arm.named_parameters())
    records = document["parameters"]
    if len(records) != len(parameters) or {r["name"] for r in records} != set(parameters):
        raise ValueError("incomplete actual parameter inventory")
    with torch.no_grad():
        for record in records:
            t = parameters[record["name"]]
            if list(t.shape) != record["shape"]:
                raise ValueError("parameter shape mismatch")
            t.zero_()
            for entry in record["nonzero"]:
                t[tuple(entry[:-1])] = entry[-1]
    arm.requires_grad_(False)
    return arm.eval()


def build_model():
    """Load the saved analytic parameters into a fresh, unmodified R9 Arm."""
    document = json.loads(Path(__file__).with_name("shared_witness.json").read_text(
        encoding="utf-8"))
    return load_weights(document)


def generate(seconds=90, output=None):
    path = Path(output) if output is not None else Path(__file__).with_name("shared_witness.json")
    if path.exists():
        raise FileExistsError(f"{path}: choose a fresh output path; published witnesses are immutable")
    torch.set_num_threads(1)
    book, first_status = two_symbol_proposal()
    coefficients, offsets = baseline_utilities(book)
    arm = construct(coefficients, offsets)
    baseline = population(arm, rational_mapping(coefficients, offsets))
    tables = decoder_tables(arm)
    proposal, second_status = shared_utility_proposal(tables, seconds)
    selected = "analytic two-symbol-per-context baseline"
    if proposal is not None:
        candidate = construct(*proposal)
        proof = margin_certificate(*proposal, candidate)
        try:
            candidate_risk = population(candidate, rational_mapping(*proposal))
        except AssertionError:
            second_status["rejected"] = "rational/runtime argmax disagreement"
        else:
            second_status["verified_candidate_joint_exact"] = candidate_risk["population_joint_exact"]
            second_status["candidate_margin_certificate"] = proof
            if (proof["strict_exact_real_argmax_certified"]
                    and F(candidate_risk["population_joint_exact"]) < F(baseline["population_joint_exact"])):
                coefficients, offsets, arm = *proposal, candidate
                selected = "bounded shared-quadratic fixed-head MILP proposal"
    result = population(arm, rational_mapping(coefficients, offsets))
    proof = margin_certificate(coefficients, offsets, arm)
    if not proof["strict_exact_real_argmax_certified"]:
        raise AssertionError("selected witness lacks an exact-real margin certificate")
    joint, specialists = F(result["population_joint_exact"]), list(map(F, result["specialists_exact"]))
    document = {
        "schema": 1, "repository_head": "e5bb8523c38b608143249e94a625628ad4f006e8",
        "scope": "constructive shared-four-context upper bound, NOT an optimum or Case-B proof",
        "training": False, "gradients": False, "stage_b": False,
        "architecture": {"arm": "R9", "width": 56, "dtype": "float32",
                         "ticks": 8, "used_hidden_units": 24, "common_trunk_context": False,
                         "encoder": "W h8 + U context + b",
                         "decoder": "affine word onehot8 + context onehot4 + ownbit"},
        "selected": selected, "zero_fill": True, "parameters": sparse_weights(arm),
        "rational_utilities": [{"coefficients": [[list(k), str(v)] for k, v in p.items()],
                               "offsets": [str(v) for v in u]}
                              for p, u in zip(coefficients, offsets)],
        "margin_certificate": proof, "population": result,
        "baseline_population": baseline,
        "bounded_attempts": [first_status, second_status],
        "gate": {"r10_exact": str(R10), "joint_threshold_exact": str(GATE),
                 "joint_threshold": float(GATE), "joint_pass": joint <= GATE,
                 "specialist_pass": [v < bound for v, bound in zip(
                     specialists, (F(1, 5), F(9, 50), F(1, 2)))],
                 "passed": joint <= GATE and all(v < bound for v, bound in zip(
                     specialists, (F(1, 5), F(9, 50), F(1, 2)))),
                 "status": "certified feasible" if joint <= GATE and all(
                     v < bound for v, bound in zip(specialists, (F(1, 5), F(9, 50), F(1, 2))))
                     else "unresolved; upper above threshold does NOT prove Case B"},
        "prior_shared_upper_exact": "8921732/29296875",
        "upper_improvement_exact": str(F(8921732, 29296875) - joint),
    }
    with path.open("x", encoding="utf-8") as stream:
        json.dump(document, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(json.dumps({k: document[k] for k in ("selected", "gate")}, indent=2))
    print(json.dumps(result | {"mapping": "256x4 stored in JSON"}, indent=2))
    return document


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=90)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    generate(args.seconds, args.output)
