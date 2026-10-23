"""Bijection between a 4-state belief and (marginals, covariance).

This is the coordinate chart of TWOSTREAM_PROTOCOL_v1.md. It is not a filter.
"""

from fractions import Fraction

from twostream_constants import state_index


def marginals_covariance(belief):
    """Return (P(X=1), P(Y=1), Cov(X,Y)) for a length-4 state-index belief."""
    p_x1 = belief[state_index(1, 0)] + belief[state_index(1, 1)]
    p_y1 = belief[state_index(0, 1)] + belief[state_index(1, 1)]
    p11 = belief[state_index(1, 1)]
    c = p11 - p_x1 * p_y1
    return p_x1, p_y1, c


def belief_from_chart(mx, my, c):
    """Inverse chart. State-index order (00, 10, 01, 11) with s = X + 2*Y."""
    p11 = mx * my + c
    p10 = mx * (1 - my) - c
    p01 = (1 - mx) * my - c
    p00 = (1 - mx) * (1 - my) + c
    belief = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    belief[state_index(0, 0)] = p00
    belief[state_index(1, 0)] = p10
    belief[state_index(0, 1)] = p01
    belief[state_index(1, 1)] = p11
    return belief


def forecasts(mx, my, c):
    """First-order forecasts of X=1, Y=1, and XOR(X,Y)=1."""
    q_x = mx
    q_y = my
    q_xor = mx + my - 2 * (mx * my + c)
    return q_x, q_y, q_xor


def in_simplex(belief):
    total = Fraction(0)
    for mass in belief:
        if mass < 0:
            return False
        total += mass
    return total == 1


def frechet_contains(mx, my, c):
    lower = max(-mx * my, -(1 - mx) * (1 - my))
    upper = min(mx * (1 - my), (1 - mx) * my)
    return lower <= c <= upper
