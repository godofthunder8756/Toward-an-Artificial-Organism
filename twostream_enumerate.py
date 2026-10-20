"""Agree Path A, Path B, and Path C on one horizon.

Used by the unit tests on short horizons and by the single certificate run
on horizons 1..8. This module imports the three paths; the paths do not
import each other.
"""

from fractions import Fraction

from twostream_chart import belief_from_chart, in_simplex, marginals_covariance
from twostream_constants import history_bits, phase_mask
from twostream_filter import filter_prefix, fraction_transition
from twostream_moments import moments_prefix
from twostream_replay import enumerate_joint_numerators


class EnumerationFailure(Exception):
    def __init__(self, failures):
        self.failures = failures
        super().__init__("; ".join(failures[:8]))


def enumerate_horizon(n_readings, failure_limit=12):
    """Return one agreed record per history, or raise EnumerationFailure."""
    matrix = fraction_transition()
    weights, denominator = enumerate_joint_numerators(n_readings)
    n_hist = 1 << n_readings
    failures = []
    numerator_total = 0
    records = []
    probability_total = Fraction(0)
    completed = True
    for history in range(n_hist):
        joint = weights[history]
        numerator = joint[0] + joint[1] + joint[2] + joint[3]
        numerator_total += numerator
        belief, probability = filter_prefix(history, n_readings, matrix)
        mx, my, c = moments_prefix(history, n_readings)
        charted = belief_from_chart(mx, my, c)
        if numerator == 0:
            failures.append("history %d has replay weight 0" % history)
        else:
            replay_belief = [Fraction(joint[s], numerator) for s in range(4)]
            replay_probability = Fraction(numerator, denominator)
            if replay_belief != belief:
                failures.append("history %d path A/B posterior mismatch" % history)
            if replay_probability != probability:
                failures.append("history %d path A/B probability mismatch" % history)
        chart_mx, chart_my, chart_c = marginals_covariance(belief)
        if charted != belief or (chart_mx, chart_my, chart_c) != (mx, my, c):
            failures.append("history %d path C/chart mismatch" % history)
        if not in_simplex(belief):
            failures.append("history %d leaves the simplex" % history)
        if probability <= 0:
            failures.append("history %d has nonpositive probability" % history)
        probability_total += probability
        records.append(
            {
                "history": history,
                "bits": history_bits(history, n_readings),
                "belief": belief,
                "prob": probability,
                "mx": mx,
                "my": my,
                "c": c,
                "joint_numerators": joint,
            }
        )
        if len(failures) >= failure_limit:
            completed = False
            break
    if completed and numerator_total != denominator:
        failures.append("joint numerators do not sum to the global denominator")
    if completed and probability_total != 1:
        failures.append("history probabilities sum to %s" % probability_total)
    if completed and not failures:
        failures.extend(symmetry_failures(records, n_readings)[:failure_limit])
    if failures:
        raise EnumerationFailure(failures)
    return {
        "n_readings": n_readings,
        "denominator": denominator,
        "records": records,
    }


def symmetry_failures(records, n_readings):
    """X-flip and Y-flip identities on a complete reachable set."""
    by_history = {row["history"]: row for row in records}
    x_mask = phase_mask(n_readings, 0)
    y_mask = phase_mask(n_readings, 1)
    failures = []
    for row in records:
        if x_mask:
            other = by_history[row["history"] ^ x_mask]
            if other["mx"] != 1 - row["mx"] or other["my"] != row["my"]:
                failures.append("X-flip marginals fail at %d" % row["history"])
            if other["c"] != -row["c"] or other["prob"] != row["prob"]:
                failures.append("X-flip covariance or probability fails at %d" % row["history"])
        if y_mask:
            other = by_history[row["history"] ^ y_mask]
            if other["my"] != 1 - row["my"] or other["mx"] != row["mx"]:
                failures.append("Y-flip marginals fail at %d" % row["history"])
            if other["c"] != -row["c"] or other["prob"] != row["prob"]:
                failures.append("Y-flip covariance or probability fails at %d" % row["history"])
        if len(failures) >= 8:
            break
    return failures
