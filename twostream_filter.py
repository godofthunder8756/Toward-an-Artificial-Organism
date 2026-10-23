"""Path A: normalized 4-state Bayes filter in exact rationals.

The transition matrix is built in this file from the (C, Dx, Dy) enumeration.
Replay and moment code must not import it.
"""

from fractions import Fraction

from twostream_constants import (
    DX,
    DY,
    E,
    G,
    state_index,
    variable_at,
)


def fraction_transition():
    """Row-stochastic transition on state index s = X + 2*Y."""
    p_c = (1 - G, G)
    p_dx = (1 - DX, DX)
    p_dy = (1 - DY, DY)
    matrix = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for x in (0, 1):
        for y in (0, 1):
            src = state_index(x, y)
            for c in (0, 1):
                for dx in (0, 1):
                    for dy in (0, 1):
                        prob = p_c[c] * p_dx[dx] * p_dy[dy]
                        dst = state_index(x ^ c ^ dx, y ^ c ^ dy)
                        matrix[src][dst] += prob
    return matrix


def initial_belief():
    return [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)]


def observe(belief, variable, bit):
    """Bayes update for one BSC reading.

    Returns (posterior, predictive probability of this bit). The predictive
    probability is the normalizer, so a product of normalizers is P(history).
    """
    if variable not in ("X", "Y"):
        raise ValueError(variable)
    if bit not in (0, 1):
        raise ValueError(bit)
    unnorm = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for s in range(4):
        x = s & 1
        y = (s >> 1) & 1
        truth = x if variable == "X" else y
        like = (1 - E) if truth == bit else E
        unnorm[s] = belief[s] * like
    predictive = unnorm[0] + unnorm[1] + unnorm[2] + unnorm[3]
    if predictive == 0:
        raise ValueError("observation has predictive probability 0")
    posterior = [mass / predictive for mass in unnorm]
    return posterior, predictive


def transit(belief, matrix):
    out = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for src in range(4):
        mass = belief[src]
        if mass == 0:
            continue
        row = matrix[src]
        for dst in range(4):
            out[dst] += mass * row[dst]
    return out


def filter_prefix(history, n_readings, matrix=None):
    """Posterior after n_readings, and P(history).

    Observe, then transition, with no transition after the last reading.
    `history` packs reading 1 in the least significant bit.
    """
    if n_readings < 1:
        raise ValueError(n_readings)
    if matrix is None:
        matrix = fraction_transition()
    belief = initial_belief()
    probability = Fraction(1)
    for t in range(n_readings):
        bit = (history >> t) & 1
        belief, predictive = observe(belief, variable_at(t), bit)
        probability *= predictive
        if t < n_readings - 1:
            belief = transit(belief, matrix)
    return belief, probability
