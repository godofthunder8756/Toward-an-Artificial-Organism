"""Inference-only exhaustive tests for analytic construction and free columns."""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path

import torch

from r10a_v1.encoder_witness import (
    HISTORIES, analytic_weight_document, construct, construct_published,
    evaluate_polynomial, exact_mapping, heldout_extension_pair,
    load_analytic_weights, risk_polynomial,
)


CODEBOOK = (
    ((0, 0), (0, 2), (0, 0)),
    ((0, 0), (2, 1), (0, 1)),
    ((0, 1), (2, 2), (1, 1)),
    ((1, 1), (0, 2), (0, 1)),
    ((1, 1), (2, 1), (0, 0)),
    ((0, 1), (2, 2), (0, 0)),
    ((0, 1), (0, 2), (1, 1)),
    ((1, 1), (2, 1), (1, 1)),
)


def independent_risk(policy, history):
    p = [Fraction(1, 17) + Fraction(15, 34) * (history[j] + history[j + 4])
         for j in range(4)]
    result = Fraction()
    for truth in product(range(2), repeat=4):
        mass = Fraction(1)
        for j, z in enumerate(truth):
            mass *= p[j] if z else 1 - p[j]
        for consumer, factor in enumerate((3, 0, 1)):
            target = truth[factor] if consumer < 2 else truth[1] ^ truth[2]
            for bit in (0, 1):
                action = policy[consumer][bit]
                loss = (Fraction(9, 50) if consumer == 1 and action == 2
                        else Fraction(action != target))
                result += mass * Fraction(4 if bit == truth[factor] else 1, 5) * loss / 3
    return result


def test_polynomial_independent_population_enumeration():
    for policy in CODEBOOK:
        coeff = risk_polynomial(policy)
        for history in HISTORIES:
            assert evaluate_polynomial(coeff, history) == independent_risk(policy, history)


def test_actual_r9_all_256_histories():
    arm, certificate = construct(CODEBOOK)
    common = torch.tensor(HISTORIES)
    with torch.no_grad():
        states = arm.encode(common)
        words, _, _, _ = arm.write(states, 4)
    assert words[:, 3].tolist() == list(exact_mapping(CODEBOOK))
    assert states.shape == (256, 56)
    assert not torch.count_nonzero(states[:, 12:])
    assert certificate["exact_real_margin_lower_bound"] > 0
    assert arm.trunk.input.in_features == 5
    assert arm.code.in_features == 60


def test_negative_s3_orientation_and_identical_word_ties():
    negative = tuple((p[0], p[1], (1, 0) if p[2] == (0, 1) else p[2])
                     for p in CODEBOOK)
    common = torch.tensor(HISTORIES)
    for codebook in (negative, (CODEBOOK[0],) * 8):
        arm, certificate = construct(codebook)
        with torch.no_grad():
            words, _, _, _ = arm.write(arm.encode(common), 4)
        assert words[:, 3].tolist() == certificate["mapping"]
    assert certificate["mapping"] == [0] * 256


def test_unused_context_columns_zero_training_gradients():
    arm, _ = construct(CODEBOOK)
    common = torch.tensor(HISTORIES)
    local = torch.tensor(list(product(range(2), repeat=3))).repeat(32, 1)
    trace = arm(common, local[:, None, :].expand(-1, 3, -1), contexts=3)
    objective = sum(logits.square().sum() for logits in trace.logits)
    # Include code logits explicitly: deterministic argmax is not differentiable.
    states = arm.encode(common)
    for context in range(3):
        onehot = torch.zeros((256, 4))
        onehot[:, context] = 1
        objective = objective + arm.code(torch.cat((states, onehot), 1)).square().sum()
    objective.backward()
    assert torch.count_nonzero(arm.code.weight.grad[:, 59]) == 0
    for head in arm.heads:
        assert torch.count_nonzero(head.weight.grad[:, 11]) == 0


def test_exact_train_agreeing_heldout_extensions():
    a, b = heldout_extension_pair()
    common = torch.tensor(HISTORIES)
    local = torch.zeros((256, 3, 3), dtype=torch.long)
    for local_pattern in product(range(2), repeat=3):
        local[:] = torch.tensor(local_pattern)
        ta, tb = a(common, local, contexts=3), b(common, local, contexts=3)
        assert torch.equal(ta.word, tb.word)
        assert all(torch.equal(x, y) for x, y in zip(ta.logits, tb.logits))
    heldout = torch.zeros((256, 4, 3), dtype=torch.long)
    ta, tb = a(common, heldout), b(common, heldout)
    assert torch.all(ta.word[:, 3] == 0)
    assert torch.all(tb.word[:, 3] == 7)
    assert torch.all(ta.actions[1][:, 3] == 2)
    assert torch.all(tb.actions[1][:, 3] == 0)
    risk_a = (Fraction(1, 5) + Fraction(9, 50) + Fraction(1, 2)) / 3
    risk_b = (Fraction(1, 5) + Fraction(1, 2) + Fraction(1, 2)) / 3
    assert risk_b - risk_a == Fraction(8, 75)


def test_published_optimal_policies_both_orientations():
    document = json.loads((Path(__file__).parent / "decoder_bounds.json").read_text())
    common = torch.tensor(HISTORIES)
    for variant in ("positive", "negative"):
        arm, certificate = construct_published(document, variant)
        codebook = [document["variants"][variant]["policies"][j]
                    for j in document["variants"][variant]["selected"]]
        with torch.no_grad():
            words, _, _, _ = arm.write(arm.encode(common), 4)
            assert words[:, 3].tolist() == certificate["mapping"]
            for consumer in range(3):
                for bit in (0, 1):
                    logits = arm.read(torch.arange(8), torch.full((8,), bit), 3, consumer)
                    assert logits.argmax(-1).tolist() == [p[consumer][bit] for p in codebook]
        assert certificate["published_mapping_matches"]
        assert Fraction(certificate["population_risk_exact"]) == Fraction(825479840, 4687500000)


def test_unrestricted_r10_encoder_only_and_weight_json_roundtrip():
    document = json.loads((Path(__file__).parent / "decoder_bounds.json").read_text())
    unrestricted = document["variants"]["unrestricted"]
    codebook = [unrestricted["policies"][j] for j in unrestricted["selected"]]
    arm, certificate = construct(codebook)
    common = torch.tensor(HISTORIES)
    counts_index = {tuple(counts): i for i, counts in enumerate(document["counts"])}
    expected = [unrestricted["encoder"][counts_index[
        tuple(h[j] + h[j + 4] for j in (3, 0, 1, 2))]] for h in HISTORIES]
    with torch.no_grad():
        assert arm.write(arm.encode(common), 4)[0][:, 3].tolist() == expected
    assert certificate["mapping"] == expected
    # This encoder assertion deliberately does NOT claim the unrestricted
    # mixed-slope S3 codebook can be implemented by the original affine heads.
    weights = analytic_weight_document(document)
    persisted = json.loads((Path(__file__).parent / "encoder_witness_weights.json").read_text())
    assert persisted == weights
    reconstructed = load_analytic_weights(persisted)
    with torch.no_grad():
        assert reconstructed.write(reconstructed.encode(common), 4)[0][:, 3].tolist() == (
            weights["certificate"]["mapping"])
        private = torch.tensor(list(product(range(2), repeat=3))).repeat(256, 1)
        trace = reconstructed(
            common.repeat_interleave(8, dim=0),
            private[:, None, :].expand(-1, 4, -1),
        )
    selected = document["variants"]["positive"]
    policies = [selected["policies"][j] for j in selected["selected"]]
    for consumer in range(3):
        expected_actions = [policies[word][consumer][int(private[row, consumer])]
                            for row, word in enumerate(trace.word[:, 3].tolist())]
        assert trace.actions[consumer][:, 3].tolist() == expected_actions
