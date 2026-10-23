"""Four-state filter, chart, and float64 continuation.

The transition and observation maps follow TWOSTREAM_PROTOCOL_v1.md.
State index s = X + 2Y. A history integer stores reading 1 in the least
significant bit. The stage-k belief is the posterior after reading k and
before the transition. A continuation u in 0..15 is readings 5–8, and
h = a + 16*u.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

G = Fraction(1, 5)
DX = Fraction(1, 50)
DY = Fraction(1, 40)
E = Fraction(1, 5)

_LIKE_FLOAT = {
    (variable, bit, s): float(
        (1 - E) if ((s & 1) if variable == "X" else ((s >> 1) & 1)) == bit else E
    )
    for variable in ("X", "Y")
    for bit in (0, 1)
    for s in range(4)
}


def state_index(x: int, y: int) -> int:
    return (x & 1) + 2 * (y & 1)


def fraction_transition():
    """Row-stochastic transition. matrix[src][dst] is P(dst | src)."""
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


def column_transition_float() -> np.ndarray:
    """Column-vector transition, float64 of the exact matrix. p' = T @ p."""
    row = fraction_transition()
    out = np.zeros((4, 4), dtype=np.float64)
    for src in range(4):
        for dst in range(4):
            out[dst, src] = float(row[src][dst])
    return out


def initial_belief():
    return [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)]


def _like_fraction(variable: str, bit: int, s: int) -> Fraction:
    x = s & 1
    y = (s >> 1) & 1
    truth = x if variable == "X" else y
    return (1 - E) if truth == bit else E


def observe_exact(belief, variable: str, bit: int):
    unnorm = [_like_fraction(variable, bit, s) * belief[s] for s in range(4)]
    predictive = unnorm[0] + unnorm[1] + unnorm[2] + unnorm[3]
    if predictive == 0:
        raise ValueError("observation has predictive probability 0")
    posterior = [mass / predictive for mass in unnorm]
    return posterior, predictive


def transit_exact(belief, matrix):
    out = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for src in range(4):
        mass = belief[src]
        if mass == 0:
            continue
        row = matrix[src]
        for dst in range(4):
            out[dst] += mass * row[dst]
    return out


def filter_prefix(history: int, n_readings: int, matrix):
    """Posterior after n_readings, and P(history). No transition after the last reading."""
    belief = initial_belief()
    probability = Fraction(1)
    for t in range(n_readings):
        bit = (history >> t) & 1
        variable = "X" if t % 2 == 0 else "Y"
        belief, predictive = observe_exact(belief, variable, bit)
        probability *= predictive
        if t < n_readings - 1:
            belief = transit_exact(belief, matrix)
    return belief, probability


def propagate_exact(belief, u: int, matrix):
    """From a stage-4 belief, apply transition/reading for readings 5–8.

    Returns the stage-8 belief and the product of the four predictive probabilities.
    """
    probability = Fraction(1)
    current = list(belief)
    for t in range(4):
        current = transit_exact(current, matrix)
        bit = (u >> t) & 1
        variable = "X" if t % 2 == 0 else "Y"
        current, predictive = observe_exact(current, variable, bit)
        probability *= predictive
    return current, probability


def marginals_covariance(belief):
    p_x1 = belief[state_index(1, 0)] + belief[state_index(1, 1)]
    p_y1 = belief[state_index(0, 1)] + belief[state_index(1, 1)]
    p11 = belief[state_index(1, 1)]
    c = p11 - p_x1 * p_y1
    return p_x1, p_y1, c


def belief_from_chart_exact(mx, my, c):
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


def forecasts_exact(mx, my, c):
    q_x = mx
    q_y = my
    q_xor = mx + my - 2 * (mx * my + c)
    return q_x, q_y, q_xor


def chart_from_belief(belief):
    mx, my, c = marginals_covariance(belief)
    mu_x = 1 - 2 * mx
    mu_y = 1 - 2 * my
    kappa = 4 * c
    return (mu_x, mu_y, kappa), (mx, my, c)


def forecasts_from_belief(belief):
    mx, my, c = marginals_covariance(belief)
    return forecasts_exact(mx, my, c)


def inverse_chart_float(theta: np.ndarray) -> np.ndarray:
    """theta = (mu_x, mu_y, kappa) -> belief (4,) float64 in state-index order."""
    mu_x, mu_y, kappa = (float(theta[0]), float(theta[1]), float(theta[2]))
    mx = (1.0 - mu_x) / 2.0
    my = (1.0 - mu_y) / 2.0
    c = kappa / 4.0
    belief = np.empty(4, dtype=np.float64)
    belief[state_index(0, 0)] = (1.0 - mx) * (1.0 - my) + c
    belief[state_index(1, 0)] = mx * (1.0 - my) - c
    belief[state_index(0, 1)] = (1.0 - mx) * my - c
    belief[state_index(1, 1)] = mx * my + c
    return belief


def _likes_float(variable: str, bit: int) -> np.ndarray:
    return np.array([_LIKE_FLOAT[(variable, bit, s)] for s in range(4)], dtype=np.float64)


def observe_float(belief: np.ndarray, variable: str, bit: int):
    unnorm = belief * _likes_float(variable, bit)
    predictive = float(unnorm.sum())
    if predictive == 0.0:
        raise ValueError("observation has predictive probability 0")
    return unnorm / predictive, predictive


def propagate_float(belief: np.ndarray, u: int, transition: np.ndarray):
    current = belief
    for t in range(4):
        current = transition @ current
        bit = (u >> t) & 1
        variable = "X" if t % 2 == 0 else "Y"
        current, _predictive = observe_float(current, variable, bit)
    return current


def forecasts_float(belief: np.ndarray) -> np.ndarray:
    """(q_X, q_Y, q_XOR) from a length-4 belief. Linear in the belief."""
    p00 = belief[0]
    p10 = belief[1]
    p01 = belief[2]
    p11 = belief[3]
    del p00
    q_x = p10 + p11
    q_y = p01 + p11
    q_xor = p10 + p01
    return np.array([q_x, q_y, q_xor], dtype=np.float64)


def phi_float(theta: np.ndarray, u: int, transition: np.ndarray):
    belief = inverse_chart_float(theta)
    terminal = propagate_float(belief, u, transition)
    return forecasts_float(terminal), terminal


def unnormalized_map(u: int, transition: np.ndarray) -> np.ndarray:
    """Linear map from the stage-4 belief to the unnormalized stage-8 mass."""
    eye = np.eye(4, dtype=np.float64)
    current = eye
    for t in range(4):
        current = transition @ current
        bit = (u >> t) & 1
        variable = "X" if t % 2 == 0 else "Y"
        current = _likes_float(variable, bit)[:, None] * current
    return current


def chart_jacobian(theta: np.ndarray) -> np.ndarray:
    """dp/d(mu_x, mu_y, kappa), shape (4, 3), at theta."""
    mu_x, mu_y, _kappa = (float(theta[0]), float(theta[1]), float(theta[2]))
    mx = (1.0 - mu_x) / 2.0
    my = (1.0 - mu_y) / 2.0
    # Columns are derivatives of (p00, p10, p01, p11) in state-index order
    # with respect to mx, my, c, then chained to (mu_x, mu_y, kappa).
    dp_dmx = np.array([-(1.0 - my), (1.0 - my), -my, my], dtype=np.float64)
    dp_dmy = np.array([-(1.0 - mx), -mx, (1.0 - mx), mx], dtype=np.float64)
    dp_dc = np.array([1.0, -1.0, -1.0, 1.0], dtype=np.float64)
    jac = np.column_stack((dp_dmx * (-0.5), dp_dmy * (-0.5), dp_dc * 0.25))
    return jac


def closed_form_L(theta: np.ndarray, u: int, transition: np.ndarray) -> np.ndarray:
    """L = d(q_X, q_Y, q_XOR)/d(mu_x, mu_y, kappa), shape (3, 3)."""
    belief = inverse_chart_float(theta)
    linear = unnormalized_map(u, transition)
    unnorm = linear @ belief
    den = float(unnorm.sum())
    if den == 0.0:
        raise ValueError("unnormalized mass is 0")
    # F @ posterior, F maps belief -> forecasts.
    # q = F @ linear @ p / (1 @ linear @ p)
    mass_row = linear.sum(axis=0)  # shape (4,)
    # Forecast rows of F @ linear.
    # q_X = p10 + p11 of the terminal posterior, i.e. components 1 and 3.
    f_rows = np.vstack((linear[1] + linear[3], linear[2] + linear[3], linear[1] + linear[2]))
    num = f_rows @ belief
    # dq/dp = (den * f_rows - outer(num, mass_row)) / den^2
    dq_dp = (den * f_rows - np.outer(num, mass_row)) / (den * den)
    return dq_dp @ chart_jacobian(theta)


def decimal_truncation_50(value: Fraction) -> str:
    negative = value < 0
    value = -value if negative else value
    scale = 10**50
    integer = value.numerator // value.denominator
    remainder = value.numerator - integer * value.denominator
    digits = (remainder * scale) // value.denominator
    body = f"{integer}.{digits:050d}"
    return f"-{body}" if negative else body


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"
