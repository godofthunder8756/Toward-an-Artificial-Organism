"""Inference-only independent checks; never invoke the proposal MILPs."""

from fractions import Fraction as F
from itertools import product
import json
from math import prod
from pathlib import Path

import torch

from shared4_v1.shared_witness import (
    GATE, HISTORIES, PAIRS, build_model, construct, decoder_tables, load_weights,
    margin_certificate, polynomial, population, rational_mapping, value,
)


DOCUMENT = json.loads(Path(__file__).with_name("shared_witness.json").read_text())


def rational_parameters():
    records = DOCUMENT["rational_utilities"]
    return ([{tuple(k): F(v) for k, v in r["coefficients"]} for r in records],
            [tuple(map(F, r["offsets"])) for r in records])


def test_complete_parameter_inventory_and_roundtrip():
    arm = load_weights(DOCUMENT)
    analytic = construct(*rational_parameters())
    assert arm.name == "R9" and arm.width == 56
    assert arm.trunk.input.in_features == 5
    assert arm.code.in_features == 60
    assert [h.in_features for h in arm.heads] == [13, 13, 13]
    assert all(not p.requires_grad for p in arm.parameters())
    assert all(torch.equal(a, b) for a, b in zip(arm.parameters(), analytic.parameters()))
    assert all(torch.isfinite(p).all() for p in arm.parameters())
    assert DOCUMENT["training"] is False and DOCUMENT["stage_b"] is False
    published = build_model()
    fresh = type(published)("R9", 56)
    fresh.load_state_dict(published.state_dict(), strict=True)
    assert all(torch.equal(a, b) for a, b in zip(fresh.parameters(), arm.parameters()))


@torch.no_grad()
def test_all_24_compiled_features_all_256_histories():
    arm = load_weights(DOCUMENT)
    state = arm.encode(torch.tensor(HISTORIES))
    expected = torch.tensor([
        [2 * h[7 - j] - 1 for j in range(8)]
        + [2 * prod(h[j] for j in pair) - 1 for pair in PAIRS]
        for h in HISTORIES], dtype=torch.float32)
    assert len(PAIRS) == len(set(PAIRS)) == 16
    assert torch.equal(state[:, :24], expected)
    assert not torch.count_nonzero(state[:, 24:])
    assert not torch.count_nonzero(arm.trunk.input.weight[:, :4])
    assert not torch.count_nonzero(arm.trunk.input.weight[24:])
    assert not torch.count_nonzero(arm.trunk.hidden.weight[24:])


@torch.no_grad()
def test_actual_runtime_all_contexts_all_private_bit_triples():
    arm = load_weights(DOCUMENT)
    patterns = tuple(product(range(2), repeat=3))
    common = torch.tensor(HISTORIES).repeat_interleave(8, 0)
    private = torch.tensor(patterns).repeat(256, 1)
    local = private[:, None, :].expand(-1, 4, -1)
    trace = arm(common, local)
    expected_words = torch.tensor(rational_mapping(*rational_parameters()))
    words = trace.word.reshape(256, 8, 4)
    assert torch.equal(words, expected_words[:, None, :].expand(-1, 8, -1))
    assert words[:, 0].tolist() == DOCUMENT["population"]["mapping"]
    tables = decoder_tables(arm)
    for i in range(3):
        expected = torch.tensor([
            [tables[c][w][i][int(private[row, i])]
             for c, w in enumerate(trace.word[row].tolist())]
            for row in range(len(common))])
        assert torch.equal(trace.actions[i], expected)
    for c in range(4):
        assert set(words[:, 0, c].tolist()) == {2 * c, 2 * c + 1}


def test_population_enumeration_256_histories_16_truths_two_readings():
    result = population(load_weights(DOCUMENT), rational_mapping(*rational_parameters()))
    assert result == DOCUMENT["population"]
    assert F(result["population_joint_exact"]) == F(1031759, 4687500)
    assert result["specialists_exact"] == ["1/5", "219259/1562500", "8/25"]
    assert result["context_joint_exact"] == ["1031759/4687500"] * 4
    assert F(result["population_joint_exact"]) < F(DOCUMENT["prior_shared_upper_exact"])


def independent_conditional_risk(policy, history, context):
    posterior = [F(1, 17) + F(15, 34) * (history[j] + history[j + 4])
                 for j in range(4)]
    risks = [F(0)] * 3
    for truth in product(range(2), repeat=4):
        mass = prod(posterior[j] if z else 1 - posterior[j]
                    for j, z in enumerate(truth))
        for i in range(3):
            factor = (context + i) % 4
            target = truth[factor] if i < 2 else truth[factor] ^ truth[(context + 3) % 4]
            for bit in (0, 1):
                a = policy[i][bit]
                loss = F(9, 50) if i == 1 and a == 2 else F(a != target)
                risks[i] += mass * F(4 if bit == truth[factor] else 1, 5) * loss
    return risks


def test_rotated_risk_polynomials_independent_truth_enumeration():
    tables = decoder_tables(load_weights(DOCUMENT))
    for c in range(4):
        for w in (2 * c, 2 * c + 1):
            coeff = polynomial(tables[c][w], c)
            for h in HISTORIES:
                assert value(coeff, h) == sum(independent_conditional_risk(
                    tables[c][w], h, c)) / 3


def test_independent_posterior_population_matches_actual_runtime():
    arm = load_weights(DOCUMENT)
    tables = decoder_tables(arm)
    mapping = DOCUMENT["population"]["mapping"]
    totals = [[F(0)] * 3 for _ in range(4)]
    mass_total = F(0)
    for history, words in zip(HISTORIES, mapping):
        mass = prod(F(17, 50) if history[j] == history[j + 4] else F(4, 25)
                    for j in range(4))
        mass_total += mass
        for c, w in enumerate(words):
            risk = independent_conditional_risk(tables[c][w], history, c)
            for i in range(3):
                totals[c][i] += mass * risk[i]
    assert mass_total == 1
    assert [[str(v) for v in row] for row in totals] == DOCUMENT[
        "population"]["context_specialists_exact"]


def test_margin_gate_and_no_impossibility_claim():
    proof = margin_certificate(*rational_parameters(), load_weights(DOCUMENT))
    assert proof == DOCUMENT["margin_certificate"]
    assert F(proof["minimum_rational_score_gap"]) > 0
    assert F(proof["exact_real_margin_lower_bound"]) > 0
    assert F(proof["conservative_float32_margin_lower_bound"]) > 0
    gate = DOCUMENT["gate"]
    assert F(gate["joint_threshold_exact"]) == GATE
    assert not gate["passed"] and not gate["joint_pass"]
    assert gate["specialist_pass"] == [False, True, True]
    assert "unresolved" in gate["status"] and "NOT prove Case B" in gate["status"]
    assert "NOT an optimum" in DOCUMENT["scope"]
    assert DOCUMENT["bounded_attempts"][1]["time_limit_seconds"] == 90
