"""Path B: direct summation over latent trajectories, in integers.

No Bayes normalization is applied during the pass. The transition numerator
is built here by enumerating (C, Dx, Dy). This module does not import the
filter or the moment recursion.
"""

from twostream_constants import latent_observed_bit, state_index

# Integer noise weights. Denominators: C out of 5, Dx out of 50, Dy out of 40.
_W_C = (4, 1)
_W_DX = (49, 1)
_W_DY = (39, 1)
TRANSITION_DENOMINATOR = 5 * 50 * 40


def integer_transition():
    """Integer transition numerators. Each row sums to TRANSITION_DENOMINATOR."""
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    for x in (0, 1):
        for y in (0, 1):
            src = state_index(x, y)
            for c in (0, 1):
                for dx in (0, 1):
                    for dy in (0, 1):
                        weight = _W_C[c] * _W_DX[dx] * _W_DY[dy]
                        dst = state_index(x ^ c ^ dx, y ^ c ^ dy)
                        matrix[src][dst] += weight
    return matrix


def global_denominator(n_readings):
    """Common denominator of every joint atom P(history, terminal state).

    Prior denominator 4, one factor of 5*50*40 per transition (n-1 of them),
    and one factor of 5 per BSC reading.
    """
    if n_readings < 1:
        raise ValueError(n_readings)
    return 4 * (TRANSITION_DENOMINATOR ** (n_readings - 1)) * (5 ** n_readings)


def enumerate_joint_numerators(n_readings):
    """Sum integer weights of all 4^n latent trajectories.

    Returns (weights, denominator). weights[h][s] is the numerator of the
    joint probability of history h and terminal state s. History bit 0 is
    reading 1. Observation integer weights are 4 on a match and 1 on a
    mismatch, applied after the latent sum by distributivity:

        sum_z w_trans(z) * prod_t 4^{1[h_t = b_t(z)]}
          = sum_b (sum_{z: bits(z)=b} w_trans(z)) * 4^{matches(h,b)}.

    Grouping by the latent observation-bit pattern does not drop or add
    trajectories. Normalization is left to the caller.
    """
    if n_readings < 1:
        raise ValueError(n_readings)
    n_hist = 1 << n_readings
    trans = integer_transition()
    grouped = [[0, 0, 0, 0] for _ in range(n_hist)]
    trajectory = [0] * n_readings
    n_trajectories = 4 ** n_readings
    for _ in range(n_trajectories):
        weight = 1
        for t in range(n_readings - 1):
            weight *= trans[trajectory[t]][trajectory[t + 1]]
        latent_bits = 0
        for t in range(n_readings):
            if latent_observed_bit(trajectory[t], t):
                latent_bits |= 1 << t
        terminal = trajectory[-1]
        grouped[latent_bits][terminal] += weight
        for t in range(n_readings):
            trajectory[t] += 1
            if trajectory[t] < 4:
                break
            trajectory[t] = 0

    weights = [[0, 0, 0, 0] for _ in range(n_hist)]
    for latent_bits in range(n_hist):
        bucket = grouped[latent_bits]
        if bucket[0] == 0 and bucket[1] == 0 and bucket[2] == 0 and bucket[3] == 0:
            continue
        for history in range(n_hist):
            matches = n_readings - (history ^ latent_bits).bit_count()
            observation_weight = 1 << (2 * matches)  # 4^matches
            row = weights[history]
            for state in range(4):
                if bucket[state]:
                    row[state] += bucket[state] * observation_weight
    return weights, global_denominator(n_readings)
