"""Phase B labels. Phase A must not call these for a headline.

Precedence is E1, then the count of invalid or collapsed seeds, then the
joint success count. The denominator stays ten.
"""

from __future__ import annotations

from first_order_control_spec import (
    CLAIM_NOT_MET,
    CLAIM_SUCCESS,
    CLAIM_UNRESOLVED_E1,
    CLAIM_UNRESOLVED_INSUFFICIENT,
    PRIMARY_NOT_MET,
    PRIMARY_REPLICATED,
    ROBUSTNESS_SENTENCE,
    SECONDARY_PREFIX,
    SHOWN_MIN,
    UNEVALUABLE_MAX,
    UNRESOLVED_E1,
    UNRESOLVED_INSUFFICIENT,
)
from graded_reversion_spec import TRANSFER_NOT_SHOWN, TRANSFER_SHOWN, UNRESOLVED


def _ten(flags) -> None:
    if len(flags) != 10:
        raise ValueError("expected 10 seeds, got %d" % len(flags))


def count_true(flags) -> int:
    _ten(flags)
    return sum(1 for flag in flags if flag is True)


def e1_replicated(e1_flags) -> bool:
    _ten(e1_flags)
    return count_true(e1_flags) >= SHOWN_MIN


def unevaluable_count(valid_flags, collapsed_flags) -> int:
    """Distinct seeds that are invalid or have a collapsed control family."""
    _ten(valid_flags)
    _ten(collapsed_flags)
    return sum(1 for valid, collapsed in zip(valid_flags, collapsed_flags) if (not valid) or collapsed)


def other_eligibility_failures(valid_flags, eligible_flags, collapsed_flags) -> int:
    """Valid, non-collapsed seeds that miss another eligibility condition."""
    _ten(valid_flags)
    _ten(eligible_flags)
    _ten(collapsed_flags)
    return sum(
        1
        for valid, eligible, collapsed in zip(valid_flags, eligible_flags, collapsed_flags)
        if valid and not collapsed and not eligible
    )


def primary_label(e1_flags, valid_flags, collapsed_flags, joint_flags) -> str:
    _ten(joint_flags)
    if not e1_replicated(e1_flags):
        return UNRESOLVED_E1
    if unevaluable_count(valid_flags, collapsed_flags) > UNEVALUABLE_MAX:
        return UNRESOLVED_INSUFFICIENT
    if count_true(joint_flags) >= SHOWN_MIN:
        return PRIMARY_REPLICATED
    return PRIMARY_NOT_MET


def secondary_label(block: str, e1_flags, valid_flags, collapsed_flags, joint_flags) -> str:
    if block not in ("r", "z", "n"):
        raise ValueError(block)
    return SECONDARY_PREFIX % block + " " + primary_label(e1_flags, valid_flags, collapsed_flags, joint_flags)


def verdict_paragraph(label: str) -> str:
    if label == PRIMARY_REPLICATED:
        return CLAIM_SUCCESS
    if label == PRIMARY_NOT_MET:
        return CLAIM_NOT_MET
    if label == UNRESOLVED_E1:
        return CLAIM_UNRESOLVED_E1
    if label == UNRESOLVED_INSUFFICIENT:
        return CLAIM_UNRESOLVED_INSUFFICIENT
    raise ValueError(label)


def transfer_label(valid_flags, transfer_flags) -> str:
    """Recurrent-core FINAL §3. Invalid seeds are not transfer passes."""
    _ten(valid_flags)
    _ten(transfer_flags)
    if sum(1 for flag in valid_flags if not flag) > UNEVALUABLE_MAX:
        return UNRESOLVED
    passed = sum(1 for valid, passed_flag in zip(valid_flags, transfer_flags) if valid and passed_flag)
    if passed >= SHOWN_MIN:
        return TRANSFER_SHOWN
    return TRANSFER_NOT_SHOWN


def robustness_applies(label: str, joint_flags, thin_fo, thin_iso) -> bool:
    """Fewer than eight joint passes are non-thin for both families."""
    if label != PRIMARY_REPLICATED:
        return False
    _ten(joint_flags)
    _ten(thin_fo)
    _ten(thin_iso)
    nonthin_both = sum(
        1
        for joint, thin_first, thin_second in zip(joint_flags, thin_fo, thin_iso)
        if joint and not thin_first and not thin_second
    )
    return nonthin_both < SHOWN_MIN


def robustness_text(label: str, joint_flags, thin_fo, thin_iso):
    if robustness_applies(label, joint_flags, thin_fo, thin_iso):
        return ROBUSTNESS_SENTENCE
    return None
