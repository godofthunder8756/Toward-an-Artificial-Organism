"""Frozen generator constants for the two-stream admission certificate.

Encoding and parameters only. No filtering, scoring, or enumeration.
The numerical values are the decision-document generator. The observation
order is the ambiguity resolved by TWOSTREAM_PROTOCOL_v1.md.
"""

from fractions import Fraction

# Decision-document generator.
G = Fraction(1, 5)  # P(C = 1), common flip
DX = Fraction(1, 50)  # P(Dx = 1), private X flip
DY = Fraction(1, 40)  # P(Dy = 1), private Y flip
E = Fraction(1, 5)  # BSC crossover on each reading
N_READINGS = 8

# Spin / moment coefficients. Derived from the generator, not free parameters.
A = 1 - 2 * G  # E[(-1)^C] = 3/5
BX = 1 - 2 * DX  # E[(-1)^Dx] = 24/25
BY = 1 - 2 * DY  # E[(-1)^Dy] = 19/20
ETA = 1 - 2 * E  # E[(-1)^noise] for a reading = 3/5

# State index s = X + 2*Y. Bit 0 is X, bit 1 is Y.
# s=0 (X,Y)=(0,0); s=1 (1,0); s=2 (0,1); s=3 (1,1).


def variable_at(t):
    """Variable observed at 0-based reading index t.

    Reading 1 (t=0) observes X, then Y, X, Y, ..., and reading 8 observes Y.
    """
    if t % 2 == 0:
        return "X"
    return "Y"


def state_index(x, y):
    return (x & 1) + 2 * (y & 1)


def state_bits(s):
    return s & 1, (s >> 1) & 1


def latent_observed_bit(state, t):
    """Latent bit of the variable observed at 0-based time t."""
    x, y = state_bits(state)
    if variable_at(t) == "X":
        return x
    return y


def phase_mask(n_readings, phase):
    """Bit mask of readings with the given phase inside a length-n prefix.

    phase 0 marks X readings (even 0-based indices). phase 1 marks Y readings.
    A zero mask means that phase has not yet been observed.
    """
    mask = 0
    for t in range(phase, n_readings, 2):
        mask |= 1 << t
    return mask


def history_bits(history, n_readings):
    """Reading-1-first bit string. Character 0 is reading 1."""
    return "".join(str((history >> t) & 1) for t in range(n_readings))
