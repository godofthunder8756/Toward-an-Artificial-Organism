"""Phase B labels. Phase A must not call these for a headline.

Precedence is E1, then the invalid-seed count, then the success count.
The denominator stays ten.
"""

from __future__ import annotations

from graded_reversion_spec import (
    CLAIM_LIMITATION,
    CLAIM_NOT_MET,
    CLAIM_SUCCESS,
    CLAIM_UNRESOLVED_E1,
    CLAIM_UNRESOLVED_INVALID,
    INVALID_MAX,
    PRIMARY_NOT_MET,
    PRIMARY_REPLICATED,
    SECONDARY_PREFIX,
    SHOWN_MIN,
    TRANSFER_NOT_SHOWN,
    TRANSFER_SHOWN,
    UNRESOLVED,
    UNRESOLVED_E1,
)


def _ten(flags) -> None:
    if len(flags) != 10:
        raise ValueError("expected 10 seeds, got %d" % len(flags))


def e1_replicated(e1_flags) -> bool:
    _ten(e1_flags)
    return sum(1 for flag in e1_flags if flag) >= SHOWN_MIN


def count_true(flags) -> int:
    _ten(flags)
    return sum(1 for flag in flags if flag)


def eligibility_failure_count(valid_flags, eligible_flags) -> int:
    """Valid seeds that miss eligibility. Invalid seeds are not in this count."""
    _ten(valid_flags)
    _ten(eligible_flags)
    return sum(
        1
        for valid, eligible in zip(valid_flags, eligible_flags)
        if valid and not eligible
    )


def precedence(e1_flags, valid_flags) -> str:
    """Which rule decides the label: e1, invalid, or success."""
    if not e1_replicated(e1_flags):
        return "e1"
    invalid = sum(1 for flag in valid_flags if not flag)
    if invalid > INVALID_MAX:
        return "invalid"
    return "success"


def primary_label(e1_flags, valid_flags, joint_flags) -> str:
    _ten(joint_flags)
    step = precedence(e1_flags, valid_flags)
    if step == "e1":
        return UNRESOLVED_E1
    if step == "invalid":
        return UNRESOLVED
    if count_true(joint_flags) >= SHOWN_MIN:
        return PRIMARY_REPLICATED
    return PRIMARY_NOT_MET


def secondary_label(e1_flags, valid_flags, joint_flags) -> str:
    return SECONDARY_PREFIX + " " + primary_label(e1_flags, valid_flags, joint_flags)


def transfer_label(valid_flags, transfer_flags) -> str:
    """Recurrent-core FINAL §3 replication count. Invalid seeds are not passes."""
    _ten(valid_flags)
    _ten(transfer_flags)
    invalid = sum(1 for flag in valid_flags if not flag)
    if invalid > INVALID_MAX:
        return UNRESOLVED
    passed = sum(1 for valid, passed in zip(valid_flags, transfer_flags) if valid and passed)
    if passed >= SHOWN_MIN:
        return TRANSFER_SHOWN
    return TRANSFER_NOT_SHOWN


def claim_text(e1_flags, valid_flags, joint_flags, directional_flags, material_flags, eligible_flags) -> str:
    step = precedence(e1_flags, valid_flags)
    if step == "e1":
        return CLAIM_UNRESOLVED_E1
    if step == "invalid":
        return CLAIM_UNRESOLVED_INVALID
    passed = count_true(joint_flags)
    if passed >= SHOWN_MIN:
        return CLAIM_SUCCESS + " " + CLAIM_LIMITATION
    return CLAIM_NOT_MET % (
        passed,
        count_true(directional_flags),
        count_true(material_flags),
        eligibility_failure_count(valid_flags, eligible_flags),
    )


def success_count_applied(e1_flags, valid_flags) -> bool:
    return precedence(e1_flags, valid_flags) == "success"
