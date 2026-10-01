"""Solver-free population arithmetic for the A6 conjunction."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import prod

COUNTS = tuple(product(range(3), repeat=4))
POLICIES = tuple(product(*(tuple(product(range(n), repeat=2)) for n in (2, 3, 2))))
COMPONENT_DENOMINATOR = 16 * 25**4 * 5 * 50
AGGREGATE_DENOMINATOR = 4 * COMPONENT_DENOMINATOR
JOINT_DENOMINATOR = 3 * AGGREGATE_DENOMINATOR
GATE = F(21579431, 117187500)
BASELINES = (F(1, 5), F(9, 50), F(1, 2))
STRICT_LIMITS = tuple(int(b * AGGREGATE_DENOMINATOR) - unit
                      for b, unit in zip(BASELINES, (50, 1, 50)))
JOINT_LIMIT = int(GATE * JOINT_DENOMINATOR)


def component_costs() -> tuple:
    rows = []
    for counts in COUNTS:
        belief = [F((1, 1, 16)[n], (17, 2, 17)[n]) for n in counts]
        weight = prod(F((17, 16, 17)[n], 50) for n in counts)
        row = []
        for policy in POLICIES:
            parts = []
            for consumer in range(3):
                q = belief[consumer]
                risk = F(0)
                for bit in (0, 1):
                    one = q * F(4 if bit else 1, 5)
                    zero = (1 - q) * F(1 if bit else 4, 5)
                    action = policy[consumer][bit]
                    if consumer == 1 and action == 2:
                        risk += F(9, 50) * (one + zero)
                    else:
                        target = (one if consumer != 2 else
                                  one * (1 - belief[3]) + zero * belief[3])
                        risk += target if action == 0 else one + zero - target
                value = weight * risk * COMPONENT_DENOMINATOR
                if value.denominator != 1:
                    raise ValueError("incorrect component population lattice")
                parts.append(value.numerator)
            row.append(tuple(parts))
        rows.append(tuple(row))
    return tuple(rows)


def conditional_lemmas() -> dict:
    q = (F(1, 17), F(1, 2), F(16, 17))
    weights = (F(17, 50), F(16, 50), F(17, 50))
    common_floor = sum(w * min(p, 1 - p) for w, p in zip(weights, q))
    assert common_floor == F(1, 5)
    assert all(F(4, 5) >= min(p, 1 - p) for p in q)
    table = component_costs()
    retained = ((0, 2), (2, 1), (2, 2))
    replacements = {}
    for source in product(range(3), repeat=2):
        original = POLICIES.index(((0, 0), source, (0, 0)))
        choices = []
        for target in retained:
            replacement = POLICIES.index(((0, 0), target, (0, 0)))
            if all(row[replacement][1] <= row[original][1] for row in table):
                choices.append(target)
        if not choices:
            raise AssertionError("S2 component-wise dominance is incomplete")
        replacements[str(source)] = list(choices[0])
    return {
        "s1_nonpositive_slope_common_floor": str(common_floor),
        "s1_nonpositive_slope_gate_impossible": True,
        "s1_reason": "allowed maps 00,10,11 have conditional risks q,4/5,1-q",
        "s2_replacements": replacements,
        "s2_scope": "valid only after dropping all S2 sharing constraints",
        "aggregate_denominator": AGGREGATE_DENOMINATOR,
        "component_numerator_units": [50, 1, 50],
        "strict_component_limits": list(STRICT_LIMITS),
        "joint_limit": JOINT_LIMIT,
        "joint_denominator": JOINT_DENOMINATOR,
    }


def gate(components: tuple[F, F, F]) -> bool:
    if len(components) != 3:
        raise ValueError("exactly three specialist losses required")
    return sum(components) / 3 <= GATE and all(
        value < baseline for value, baseline in zip(components, BASELINES))
