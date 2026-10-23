"""Path C: closed-form (marginal, covariance) recursion.

The maps are the rational updates proved in TWOSTREAM_PROTOCOL_v1.md.
This module does not import the 4-state filter or the latent-path replay.
"""

from fractions import Fraction

from twostream_constants import A, BX, BY, E, ETA, variable_at


def initial_moments():
    return Fraction(1, 2), Fraction(1, 2), Fraction(0)


def _predictive(m_obs, bit):
    p1 = E + ETA * m_obs
    if bit == 1:
        return p1
    return 1 - p1


def observe_moments(mx, my, c, variable, bit):
    """One reading. Covariance is rescaled and is never created from zero."""
    if variable == "X":
        m_obs, m_other = mx, my
    elif variable == "Y":
        m_obs, m_other = my, mx
    else:
        raise ValueError(variable)
    predictive = _predictive(m_obs, bit)
    if bit == 1:
        m_obs_2 = (1 - E) * m_obs / predictive
        m_other_2 = m_other + ETA * c / predictive
    else:
        m_obs_2 = E * m_obs / predictive
        m_other_2 = m_other - ETA * c / predictive
    c_2 = E * (1 - E) * c / (predictive * predictive)
    if variable == "X":
        return m_obs_2, m_other_2, c_2
    return m_other_2, m_obs_2, c_2


def transit_moments(mx, my, c):
    """One hidden transition. The common flip can create covariance."""
    half = Fraction(1, 2)
    mx_2 = half + A * BX * (mx - half)
    my_2 = half + A * BY * (my - half)
    created = (1 - A * A) * (mx - half) * (my - half)
    c_2 = BX * BY * (c + created)
    return mx_2, my_2, c_2


def moments_prefix(history, n_readings):
    """Terminal (or prefix) moments. No transition after the last reading."""
    if n_readings < 1:
        raise ValueError(n_readings)
    mx, my, c = initial_moments()
    for t in range(n_readings):
        bit = (history >> t) & 1
        mx, my, c = observe_moments(mx, my, c, variable_at(t), bit)
        if t < n_readings - 1:
            mx, my, c = transit_moments(mx, my, c)
    return mx, my, c
