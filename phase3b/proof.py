"""Exact H3 map enumeration, checked before any neural fitting."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import prod

import torch

from phase3b.world import loss_units


def posterior(n: int, local: int) -> Fraction:
    odds = Fraction(4) ** (2 * n - 2 + 2 * local - 1)
    return odds / (1 + odds)


def parity_probability(a: Fraction, b: Fraction) -> Fraction:
    return a * (1 - b) + (1 - a) * b


def bayes_action(which: int, n: tuple[int, int, int, int], bit: int) -> int:
    if which == 0:
        return int(posterior(n[0], bit) > Fraction(1, 2))
    if which == 1:
        q = posterior(n[1], bit)
        losses = (q, 1 - q, Fraction(9, 50))
        return min(range(3), key=lambda a: (losses[a], a))
    q = parity_probability(posterior(n[2], bit),
                           Fraction((1, 8, 16)[n[3]], (17, 16, 17)[n[3]]))
    return int(q > Fraction(1, 2))


def verify_h3() -> dict[str, int]:
    """27 distinct two-local-bit policy triples, all with positive support."""
    # Derive each conditional risk independently from the actual evaluator
    # loss ledger. Truth/posterior appear only inside this pretraining proof.
    truths = list(product((0, 1), repeat=4))
    raw = torch.tensor(truths, dtype=torch.long)
    ledger: dict[tuple[int, int], list[int]] = {}
    for consumer, size in ((0, 2), (1, 3), (2, 2)):
        for action in range(size):
            acts = [torch.zeros(16, 3, dtype=torch.long) for _ in range(3)]
            acts[consumer][:, 0] = action
            ledger[consumer, action] = loss_units(tuple(acts), raw)[:, 0, consumer].tolist()
    policies = set()
    for a, b, c in product(range(3), repeat=3):
        n = (a, b, c, 2)
        for bit in (0, 1):
            for consumer, size in ((0, 2), (1, 3), (2, 2)):
                q = [Fraction((1, 8, 16)[v], (17, 16, 17)[v]) for v in n]
                target = consumer if consumer != 2 else 2
                q[target] = posterior(n[target], bit)
                probabilities = [prod(q[j] if z[j] else 1 - q[j] for j in range(4))
                                 for z in truths]
                risks = [sum(p * value for p, value in zip(probabilities, ledger[consumer, action]))
                         for action in range(size)]
                if bayes_action(consumer, n, bit) != min(range(size), key=lambda act: (risks[act], act)):
                    raise AssertionError("H3 Bayes map contradicts implemented losses; STOP")
        policies.add(tuple(tuple(bayes_action(i, n, bit) for bit in (0, 1))
                           for i in range(3)))
    if len(policies) != 27 or len(policies) <= 8:
        raise AssertionError("H3 scarcity proof failed; STOP")
    for i in range(3):
        if len({p[i] for p in policies}) != 3:
            raise AssertionError("specialist map collapse; STOP")
    # A=(2,1,1,1), B=(1,2,1,1); both have identical present observations.
    history_a: tuple[int, int, int, int] = (2, 1, 1, 1)
    history_b: tuple[int, int, int, int] = (1, 2, 1, 1)
    if (bayes_action(0, history_a, 0), bayes_action(0, history_b, 0)) != (1, 0):
        raise AssertionError("matched-history S1 witness failed; STOP")
    if (bayes_action(1, history_a, 1), bayes_action(1, history_b, 1)) != (2, 1):
        raise AssertionError("matched-history S2 witness failed; STOP")
    return {"policy_triples": len(policies), "legal_words": 8}