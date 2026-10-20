"""Brier excess, admission gates, and storage accounting.

Thresholds are the decision-document values. Comparisons use exact rationals.
"""

from fractions import Fraction

from twostream_chart import forecasts
from twostream_constants import E


# Frozen thresholds. Do not retune after seeing enumeration output.
XOR_EXCESS_THRESHOLD = Fraction(1, 1000)
XOR_SHIFT_THRESHOLD = Fraction(1, 20)
INTERVENTION_MASS_THRESHOLD = Fraction(1, 4)
COVARIANCE_SHIFT_THRESHOLD = XOR_SHIFT_THRESHOLD / 2  # |c| >= 1/40


def xor_forecasts(mx, my, c):
    _qx, _qy, q_xor = forecasts(mx, my, c)
    return q_xor


def factorized_xor(mx, my):
    return mx + my - 2 * mx * my


def expected_squared_error(probabilities, forecasts_arm, forecasts_oracle):
    """E[(q - q*)^2] under the history law. This is the Brier excess."""
    total = Fraction(0)
    for prob, q_arm, q_oracle in zip(probabilities, forecasts_arm, forecasts_oracle):
        gap = q_arm - q_oracle
        total += prob * gap * gap
    return total


def irreducible_brier(probabilities, forecasts_oracle):
    """E[q*(1-q*)], the one-component Bayes risk of the oracle."""
    total = Fraction(0)
    for prob, q_oracle in zip(probabilities, forecasts_oracle):
        total += prob * q_oracle * (1 - q_oracle)
    return total


def intervention_mass(probabilities, covariances):
    """History mass on which |q_factorized - q_joint| >= 1/20.

    The absolute forecast change equals 2|c|, so the event is |c| >= 1/40.
    """
    mass = Fraction(0)
    for prob, c in zip(probabilities, covariances):
        if abs(c) >= COVARIANCE_SHIFT_THRESHOLD:
            mass += prob
    return mass


def current_only_terminal(last_y_bit):
    """Known-model posterior given only reading 8, which observes Y.

    The unconditional terminal prior is uniform and independent, so
    P(X=1 | O8) = 1/2, Cov = 0, and P(Y=1 | O8=1) = 1-e, P(Y=1 | O8=0) = e.
    """
    if last_y_bit not in (0, 1):
        raise ValueError(last_y_bit)
    my = (1 - E) if last_y_bit == 1 else E
    return Fraction(1, 2), my, Fraction(0)


def gate_i_pass(history_excess):
    return history_excess > 0


def gate_ii_pass(xor_excess):
    return xor_excess >= XOR_EXCESS_THRESHOLD


def gate_iii_pass(mass, xy_unchanged):
    return bool(xy_unchanged) and mass >= INTERVENTION_MASS_THRESHOLD


def gate_iv_pass(mismatches):
    return mismatches == 0


def classify_run(integrity_failures, gates):
    """Admission verdict from the frozen rule.

    Gate (iv) is an identity check. Any integrity failure, including a failed
    identity check, yields UNRESOLVED. REJECT is available only when the
    implementation checks hold and at least one of gates (i), (ii), (iii) misses
    its scientific threshold. A nonpositive gate-(i) value is recorded as an
    integrity failure by the runner because it contradicts the frozen sign proof.
    """
    if integrity_failures or not gates["iv"]:
        return "UNRESOLVED"
    if gates["i"] and gates["ii"] and gates["iii"]:
        return "ADMIT"
    return "REJECT"


def fraction_bit_lengths(value):
    value = Fraction(value)
    return value.numerator.bit_length(), value.denominator.bit_length()


def decimal_truncation(value, digits=50):
    """Truncated base-10 expansion. A trailing '...' means a nonzero remainder."""
    value = Fraction(value)
    if value == 0:
        return "0." + ("0" * digits)
    sign = "-" if value < 0 else ""
    value = abs(value)
    whole = value.numerator // value.denominator
    remainder = value.numerator % value.denominator
    chars = []
    for _ in range(digits):
        remainder *= 10
        digit, remainder = divmod(remainder, value.denominator)
        chars.append(str(digit))
    suffix = "" if remainder == 0 else "..."
    return sign + str(whole) + "." + "".join(chars) + suffix


def fraction_record(value, digits=50):
    value = Fraction(value)
    num_bits, den_bits = fraction_bit_lengths(value)
    return {
        "exact": "%s/%s" % (value.numerator, value.denominator),
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "numerator_bits": num_bits,
        "denominator_bits": den_bits,
        "decimal_truncation_50": decimal_truncation(value, digits),
    }

