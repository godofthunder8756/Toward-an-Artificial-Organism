"""Analytic R9 witnesses: no training, optimizer, or history lookup in inference."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import exp, lcm

import torch
from phase3b.models import Arm


CONTEXT = 3
GAIN = 32
PAIRS = ((1, 2), (1, 6), (5, 2), (5, 6))
HISTORIES = tuple(product(range(2), repeat=8))
RISK_DENOMINATOR = 867000


def _conditional_loss(policy, truth, consumer, other=0):
    target = truth if consumer < 2 else truth ^ other
    return sum(
        F(4 if bit == truth else 1, 5)
        * (F(9, 50) if consumer == 1 and policy[bit] == 2
           else F(policy[bit] != target))
        for bit in (0, 1)
    )


def risk_polynomial(policy):
    """Exact joint-risk coefficients on raw bits and four pairwise ANDs.

    Context 3 targets are factor 3, factor 0, and factor 1 XOR factor 2.
    The last consumer's private bit observes factor 1, not the parity.
    """
    if len(policy) != 3 or any(
        len(p) != 2 or any(a not in range(n) for a in p)
        for p, n in zip(policy, (2, 3, 2))
    ):
        raise ValueError("expected three legal two-local-bit action maps")
    coeff = {(): F(0)}

    def add(key, value):
        key = tuple(sorted(key))
        coeff[key] = coeff.get(key, F(0)) + value / 3

    def add_p(factor, scale):
        add((), scale / 17)
        for bit in (factor, factor + 4):
            add((bit,), scale * F(15, 34))

    for consumer, factor in ((0, 3), (1, 0)):
        zero, one = (_conditional_loss(policy[consumer], z, consumer)
                     for z in (0, 1))
        add((), zero)
        add_p(factor, one - zero)
    table = {(a, b): _conditional_loss(policy[2], a, 2, b)
             for a, b in product(range(2), repeat=2)}
    cross = table[1, 1] - table[1, 0] - table[0, 1] + table[0, 0]
    add((), table[0, 0])
    add_p(1, table[1, 0] - table[0, 0])
    add_p(2, table[0, 1] - table[0, 0])
    add((), cross / 289)
    for bit in (1, 5, 2, 6):
        add((bit,), cross * F(15, 578))
    for pair in PAIRS:
        add(pair, cross * F(225, 1156))
    return {key: value for key, value in coeff.items() if value}


def evaluate_polynomial(coeff, history):
    return sum(value * product_value(history, key)
               for key, value in coeff.items())


def product_value(history, key):
    value = 1
    for bit in key:
        value *= history[bit]
    return value


def exact_mapping(codebook):
    polynomials = tuple(risk_polynomial(p) for p in codebook)
    return tuple(min(range(len(codebook)),
                     key=lambda w: (evaluate_polynomial(polynomials[w], h), w))
                 for h in HISTORIES)


def construct(codebook):
    """Return an actual width-56 R9 Arm and exact-real margin certificate.

    Only the context-3 encoder policy is certified. Decoder installation is
    intentionally separate: a codebook must independently pass affine-head
    feasibility. Other contexts are not asserted optimal.
    """
    codebook = tuple(tuple(tuple(p) for p in word) for word in codebook)
    if len(codebook) != 8:
        raise ValueError("the eight output words require eight supplied policies")
    polynomials = tuple(risk_polynomial(p) for p in codebook)
    lattice = lcm(*(value.denominator for p in polynomials for value in p.values()))
    scale = 16 * lattice
    positive_gaps = []
    for history in HISTORIES:
        values = sorted(set(evaluate_polynomial(p, history) for p in polynomials))
        if any((v * RISK_DENOMINATOR).denominator != 1 for v in values):
            raise AssertionError("conditional-risk denominator bound failed")
        positive_gaps.extend(b - a for a, b in zip(values, values[1:]))
    gap = min(positive_gaps, default=F(1))
    epsilon = F(1, scale)
    coefficient_bound = max(sum(abs(v) for key, v in p.items() if key)
                            for p in polynomials)
    # Legitimate delayed bits and conjunctions each have signed error <= E.
    error_bound = 2 * exp(-62)
    logit_error_bound = scale * float(coefficient_bound) * error_bound / 2
    # e^3 > 20 (Taylor terms through degree 8), e^2 > 3, hence
    # 2 e^-62 < 1/10^26. Keep a genuinely exact margin as well as display floats.
    exact_margin = 1 - scale * coefficient_bound * F(1, 10**26)
    if 2 * logit_error_bound >= 1:
        raise AssertionError("analytic tanh margin does not dominate error")

    arm = Arm("R9", 56)
    with torch.no_grad():
        for parameter in arm.parameters():
            parameter.zero_()
        arm.trunk.input.weight[0, 4] = 2 * GAIN
        arm.trunk.input.bias[0] = -GAIN
        for delay in range(1, 8):
            arm.trunk.hidden.weight[delay, delay - 1] = GAIN
        for unit, pair in enumerate(PAIRS, 8):
            arm.trunk.input.bias[unit] = -GAIN
            for bit in pair:
                # h7's delay 0 contains bit 6.
                arm.trunk.hidden.weight[unit, 6 - bit] = GAIN
        for word, coeff in enumerate(polynomials):
            bias = -scale * coeff.get((), F(0)) - word
            for key, value in coeff.items():
                if not key:
                    continue
                unit = 7 - key[0] if len(key) == 1 else (
                    8 + tuple(tuple(sorted(p)) for p in PAIRS).index(key))
                weight = -scale * value / 2
                assert weight.denominator == 1
                arm.code.weight[word, unit] = float(weight)
                bias += weight
            assert bias.denominator == 1
            arm.code.bias[word] = float(bias)
        # These integers, including all possible partial dot-product sums,
        # are exactly representable in the actual float32 code module.
        integer_sum_bound = float(
            (arm.code.weight.abs().sum(1) + arm.code.bias.abs()).max())
        if integer_sum_bound >= 2**24:
            raise AssertionError("float32 exact-integer head bound failed")
    return arm, {
        "context": CONTEXT,
        "gain": GAIN,
        "used_hidden_units": 12,
        "minimum_positive_risk_gap": str(gap),
        "lexicographic_epsilon": str(epsilon),
        "coefficient_lattice_denominator": lattice,
        "integer_score_scale": scale,
        "integer_head_absolute_sum_bound": integer_sum_bound,
        "coefficient_l1_bound": str(coefficient_bound),
        "signed_feature_error_bound": error_bound,
        "logit_error_bound": logit_error_bound,
        "exact_real_margin_lower_bound": float(exact_margin) - 2**-52,
        "exact_real_margin_rational_lower_bound": str(exact_margin),
        "mapping": list(exact_mapping(codebook)),
        "scope": "one-context Bayes assignment for supplied codebook; not decoder feasibility",
    }


def heldout_extension_pair():
    """Exactly train-agreeing finite R9 parameters, heldout risk gap 8/75."""
    arms = (Arm("R9", 56), Arm("R9", 56))
    with torch.no_grad():
        for arm in arms:
            for parameter in arm.parameters():
                parameter.zero_()
            for consumer in (0, 2):
                arm.heads[consumer].bias[1] = -1
                arm.heads[consumer].weight[1, 12] = 2
            arm.heads[1].bias[2] = 1
        # Encoder contexts use columns width + c; decoder contexts use 8 + c.
        arms[1].code.weight[7, 56 + 3] = 2
        arms[1].heads[1].weight[0, 8 + 3] = 2
    return arms


def install_reduced_decoders(arm, codebook):
    """Install finite affine heads for the certified reduced 27-map alphabet."""
    with torch.no_grad():
        for head in arm.heads:
            head.weight.zero_()
            head.bias.zero_()
        for consumer in (0, 2):
            maps = {tuple(word[consumer]) for word in codebook}
            if (0, 1) in maps and (1, 0) in maps:
                raise ValueError("one affine binary head cannot have both slopes")
            inverse = (1, 0) in maps
            intercepts = ({(0, 0): -1, (1, 0): 1, (1, 1): 3} if inverse
                          else {(0, 0): -3, (0, 1): -1, (1, 1): 1})
            arm.heads[consumer].weight[1, 12] = -2 if inverse else 2
            for word, policy in enumerate(codebook):
                arm.heads[consumer].weight[1, word] = intercepts[tuple(policy[consumer])]
        ternary = {(0, 2): (1, -4, 0),
                   (2, 1): (-4, 0, 1),
                   (2, 2): (-4, -4, 1)}
        arm.heads[1].weight[:, 12] = torch.tensor((0, 4, 2))
        for word, policy in enumerate(codebook):
            arm.heads[1].weight[:, word] = torch.tensor(ternary[tuple(policy[1])])


def construct_published(document, variant="positive"):
    """Bind the analytic witness to the immutable decoder-bound document."""
    if variant not in ("positive", "negative"):
        raise ValueError("only affine-feasible reduced variants are certified")
    published = document["variants"][variant]
    codebook = tuple(published["policies"][j] for j in published["selected"])
    arm, certificate = construct(codebook)
    install_reduced_decoders(arm, codebook)
    counts_index = {tuple(counts): i for i, counts in enumerate(document["counts"])}
    numerator_risk = F(0)
    for history, word in zip(HISTORIES, certificate["mapping"]):
        # The solver's relative factors 0,1,2,3 rotate to 3,0,1,2 at context 3.
        counts = tuple(history[j] + history[j + 4] for j in (3, 0, 1, 2))
        if word != published["encoder"][counts_index[counts]]:
            raise AssertionError("published lowest-word assignment differs")
        mass = F(1)
        for j in range(4):
            mass *= F(17, 50) if history[j] == history[j + 4] else F(4, 25)
        numerator_risk += mass * evaluate_polynomial(risk_polynomial(codebook[word]), history)
    expected = F(published["numerator"], document["denominator"])
    if numerator_risk != expected:
        raise AssertionError("published population objective differs")
    certificate.update({
        "variant": variant,
        "population_risk_exact": str(numerator_risk),
        "published_numerator": published["numerator"],
        "published_denominator": document["denominator"],
        "published_mapping_matches": True,
        "decoder_installed": True,
        "scope": "complete deployed R9 context-3 policy; other contexts not optimality-certified",
    })
    return arm, certificate


def analytic_weight_document(document, variant="positive"):
    """JSON-serializable sparse, complete, analytically derived actual weights."""
    arm, certificate = construct_published(document, variant)
    parameters = []
    for name, tensor in arm.named_parameters():
        entries = []
        for index in torch.nonzero(tensor, as_tuple=False).tolist():
            value = float(tensor[tuple(index)].detach())
            if not value.is_integer():
                raise AssertionError("the published witness uses only integer weights")
            entries.append(index + [int(value)])
        parameters.append({"name": name, "shape": list(tensor.shape), "nonzero": entries})
    return {
        "schema": 1,
        "provenance": "analytic finite weights; no training or fitted parameters",
        "architecture": {"arm": "R9", "width": 56, "dtype": "float32",
                         "ticks": 8, "initial_hidden": 0},
        "zero_fill": True,
        "parameters": parameters,
        "certificate": certificate,
    }


def load_analytic_weights(document):
    """Reconstruct the published sparse weights without the codebook solver."""
    if document["architecture"] != {
        "arm": "R9", "width": 56, "dtype": "float32",
        "ticks": 8, "initial_hidden": 0,
    } or not document["zero_fill"]:
        raise ValueError("unsupported analytic witness architecture")
    arm = Arm("R9", 56)
    actual = dict(arm.named_parameters())
    records = document["parameters"]
    if {p["name"] for p in records} != set(actual) or len(records) != len(actual):
        raise ValueError("incomplete parameter inventory")
    with torch.no_grad():
        for record in records:
            tensor = actual[record["name"]]
            if record["shape"] != list(tensor.shape):
                raise ValueError("parameter shape mismatch")
            tensor.zero_()
            for entry in record["nonzero"]:
                tensor[tuple(entry[:-1])] = entry[-1]
    return arm
