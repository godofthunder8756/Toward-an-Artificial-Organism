"""Per-seed flags, margins, and the thin-margin rule.

These functions do not train and do not build paths. Thresholds are the
protocol's. A missing curve is None, which is not a pass.
"""

from __future__ import annotations

import math

from graded_reversion_outcomes import d_passes, eligibility, m_passes
from graded_reversion_spec import EPS0
from first_order_control_spec import (
    FAMILY_FO,
    FAMILY_ISO,
    N_PATHS,
    THIN_REL,
    UNDEFINED,
)


def fo_auc_from_dot(inner: float) -> float:
    """AUC of the initial tangent. Sum of dose-weight times alpha is 1/2."""
    if not math.isfinite(inner):
        raise ValueError("non-finite inner product")
    return float(inner) / 2.0


def eligibility_target(valid, transfer, b_prefix, c_prefix, displacement, collapsed) -> tuple[bool, list]:
    ok, reasons = eligibility(valid, transfer, b_prefix, c_prefix, displacement)
    if collapsed:
        return False, list(reasons) + ["collapsed"]
    return ok, list(reasons)


def d_family(auc_rev, family_aucs) -> bool:
    if auc_rev is None:
        return False
    return bool(d_passes(float(auc_rev), family_aucs))


def m_flag(auc_rev, b_prefix) -> bool:
    if auc_rev is None or b_prefix is None:
        return False
    return bool(m_passes(float(auc_rev), float(b_prefix)))


def joint_pass(valid, eligible, d_fo, d_iso, material) -> bool:
    return bool(valid and eligible and d_fo and d_iso and material)


def percentage_undefined(max_auc) -> bool:
    if max_auc is None or not math.isfinite(float(max_auc)):
        return True
    return not (float(max_auc) > EPS0)


def is_thin(joint: bool, margin, max_auc) -> bool:
    """Thin is per family and only for a joint-passing seed with a positive max."""
    if not joint or margin is None or percentage_undefined(max_auc):
        return False
    return bool(float(margin) < THIN_REL * float(max_auc))


def rank_of_rev(rev_value: float, others) -> int:
    """1-based rank among 1+32. Exact ties count against REV."""
    if len(others) != N_PATHS:
        raise ValueError(len(others))
    ahead = sum(1 for value in others if float(value) >= float(rev_value))
    return 1 + ahead


def _finite_number(value):
    if value is None:
        return None
    number = float(value)
    if not math.isfinite(number):
        return None
    return number


def ratio_or_undefined(numerator, denominator):
    num = _finite_number(numerator)
    den = _finite_number(denominator)
    if num is None or den is None or not (den > EPS0):
        return UNDEFINED
    return float(num / den)


def endpoint_counts(rev_endpoint, family_endpoints) -> dict:
    if len(family_endpoints) != N_PATHS:
        raise ValueError(len(family_endpoints))
    rev = _finite_number(rev_endpoint)
    if rev is None or any(_finite_number(value) is None for value in family_endpoints):
        return {
            "n_end_gt": None,
            "n_end_tie": None,
            "endpoint_D": None,
            "max_endpoint": None,
        }
    greater = 0
    ties = 0
    for value in family_endpoints:
        gap = float(value) - rev
        if gap > EPS0:
            greater += 1
        if abs(gap) <= EPS0:
            ties += 1
    maximum = max(float(value) for value in family_endpoints)
    return {
        "n_end_gt": greater,
        "n_end_tie": ties,
        "endpoint_D": bool((rev - maximum) > EPS0),
        "max_endpoint": maximum,
    }


def family_margin_report(
    auc_rev,
    family_aucs,
    rev_deltas,
    family_deltas,
    b_prefix,
    pd_value,
    joint: bool,
) -> dict:
    """§6.1 columns for one family. family_deltas is a list of 32 length-6 series."""
    if len(family_aucs) != N_PATHS:
        raise ValueError(len(family_aucs))
    finite = (
        _finite_number(auc_rev) is not None
        and all(_finite_number(value) is not None for value in family_aucs)
    )
    if not finite:
        return {
            "margin": None,
            "m_over_B": UNDEFINED,
            "m_over_PD": UNDEFINED,
            "m_over_max": UNDEFINED,
            "max_auc": None,
            "median_auc": None,
            "aucs": [ _finite_number(value) for value in family_aucs ],
            "rank": None,
            "per_dose_rank": None,
            "n_end_gt": None,
            "n_end_tie": None,
            "endpoint_D": None,
            "thin": False,
            "percentage_undefined": True,
            "D": False,
        }
    maximum = max(float(value) for value in family_aucs)
    margin = float(auc_rev) - maximum
    ordered = sorted(float(value) for value in family_aucs)
    median = 0.5 * (ordered[15] + ordered[16])
    dose_ranks = None
    ends = {
        "n_end_gt": None,
        "n_end_tie": None,
        "endpoint_D": None,
        "max_endpoint": None,
    }
    if rev_deltas is not None and family_deltas is not None:
        dose_ranks = {}
        for index, alpha in enumerate((0.125, 0.25, 0.5, 0.75, 1.0)):
            column = [series[index + 1] for series in family_deltas]
            dose_ranks[str(alpha)] = rank_of_rev(rev_deltas[index + 1], column)
        ends = endpoint_counts(rev_deltas[-1], [series[-1] for series in family_deltas])
    undefined = percentage_undefined(maximum)
    return {
        "margin": margin,
        "m_over_B": ratio_or_undefined(margin, b_prefix),
        "m_over_PD": ratio_or_undefined(margin, pd_value),
        "m_over_max": UNDEFINED if undefined else float(margin / maximum),
        "max_auc": maximum,
        "median_auc": median,
        "aucs": [float(value) for value in family_aucs],
        "rank": rank_of_rev(float(auc_rev), family_aucs),
        "per_dose_rank": dose_ranks,
        "n_end_gt": ends["n_end_gt"],
        "n_end_tie": ends["n_end_tie"],
        "endpoint_D": ends["endpoint_D"],
        "thin": is_thin(joint, margin, maximum),
        "percentage_undefined": undefined,
        "D": bool((margin > EPS0)),
    }


def materiality_ratio(auc_rev, b_prefix):
    if _finite_number(auc_rev) is None or _finite_number(b_prefix) is None:
        return None
    quarter = float(b_prefix) / 4.0
    if quarter == 0.0 or not math.isfinite(quarter):
        return None
    return float(float(auc_rev) / quarter)


def margin_sentence(thin_count: int, joint_count: int, undefined_count: int, strict_seeds: int, tie_seeds: int, endpoint_pass_seeds: int, family: str) -> str:
    if family not in (FAMILY_FO, FAMILY_ISO):
        raise ValueError(family)
    return (
        "%d of %d joint-passing seeds exceed the most damaging sampled %s path by less than 10%% of that path's AUC "
        "(%d seeds with this percentage undefined because that family's maximum AUC is ≤ eps0). "
        "At alpha = 1, at least one sampled %s path causes strictly greater loss than reversion in %d/10 seeds, "
        "and at least one ties it within eps0 in %d/10 seeds. "
        "The preregistered directional criterion concerns trapezoidal AUC over the dose grid; "
        "an endpoint-only directional comparison against this family would pass in %d/10 seeds. "
        "These descriptive findings do not change the frozen labels."
        % (
            thin_count,
            joint_count,
            family,
            undefined_count,
            family,
            strict_seeds,
            tie_seeds,
            endpoint_pass_seeds,
        )
    )
