"""Preregistered labels. Inputs are per-seed booleans and measured numbers.

Counting rule used everywhere a protocol threshold is 8/10: an invalid seed
is not a pass, and more than 2 invalid seeds makes the label UNRESOLVED.
"""

from __future__ import annotations

import math

from recurrent_core_transfer_spec import (
    ADVANTAGE_NOT,
    ADVANTAGE_OBSERVED,
    CLAIM_FIRST_SENTENCE,
    CLAIM_REVERSION_FAIL,
    CLAIM_REVERSION_UNRESOLVED,
    CLAIM_SUCCESS,
    E1_REPLICATED,
    E1_UNRESOLVED,
    EPS0,
    HALF,
    INVALID_MAX,
    N_RANDOM,
    Q7_REVERSION,
    Q7_TRANSFER,
    Q7_TUNED,
    RIVAL_AFIT,
    RIVAL_AFIT_NOT,
    SHOWN_MIN,
    THREE_QUARTERS,
    TRANSFER_NOT_SHOWN,
    TRANSFER_SHOWN,
    UNRESOLVED,
    VARIATION_FAIL,
    VARIATION_OK,
    specific_name,
)
from twostream_acquisition_e3_v2 import UNDEFINED, e3_v2_meets, e3_v2_ratio


def transfer_pass(valid: bool, afit: bool, e_trained: float, e_init: float) -> bool:
    """Direct inequality. Not the E3-v2 ratio function."""
    if not valid or not afit:
        return False
    if not math.isfinite(e_trained) or not math.isfinite(e_init):
        return False
    return bool(e_trained <= HALF * e_init)


def specific_joint(transfer: bool, benefit: float, delta: float, random_deltas, delta_norm: float) -> bool:
    if not transfer:
        return False
    if not math.isfinite(benefit) or benefit <= EPS0:
        return False
    if not math.isfinite(delta_norm) or delta_norm <= EPS0:
        return False
    if not math.isfinite(delta) or not (delta > EPS0 and delta >= benefit / 4.0):
        return False
    if len(random_deltas) != N_RANDOM:
        return False
    for random_delta in random_deltas:
        if not math.isfinite(random_delta) or not (delta > random_delta):
            return False
    return True


def ratio_value(numerator: float, denominator: float):
    if not math.isfinite(numerator) or not math.isfinite(denominator):
        return UNDEFINED
    return e3_v2_ratio(numerator, denominator)


def ratio_at_most_half(numerator: float, denominator: float) -> bool:
    return bool(e3_v2_meets(ratio_value(numerator, denominator), HALF, at_least=False))


def pdcd_passes(ratio, bound: float, at_least: bool) -> bool:
    return bool(e3_v2_meets(ratio, bound, at_least=at_least))


def variation_joint(section5_valid: bool, pr, pr_random, cr) -> bool:
    if not section5_valid:
        return False
    if not pdcd_passes(pr, HALF, at_least=False):
        return False
    if not pdcd_passes(cr, THREE_QUARTERS, at_least=True):
        return False
    if len(pr_random) != N_RANDOM:
        return False
    for other in pr_random:
        if other is UNDEFINED or pr is UNDEFINED:
            return False
        if not (pr < other):
            return False
    return True


def _count(flags) -> tuple[int, int]:
    if len(flags) != 10:
        raise ValueError("expected 10 seeds, got %d" % len(flags))
    invalid = sum(1 for valid, _passed in flags if not valid)
    passed = sum(1 for valid, passed in flags if valid and passed)
    return invalid, passed


def eight_label(flags, shown: str, failed: str) -> str:
    invalid, passed = _count(flags)
    if invalid > INVALID_MAX:
        return UNRESOLVED
    if passed >= SHOWN_MIN:
        return shown
    return failed


def label_e1(replicated_flags: list[bool]) -> str:
    if len(replicated_flags) != 10:
        raise ValueError(len(replicated_flags))
    if sum(1 for flag in replicated_flags if flag) >= SHOWN_MIN:
        return E1_REPLICATED
    return E1_UNRESOLVED


def label_transfer(flags) -> str:
    return eight_label(flags, TRANSFER_SHOWN, TRANSFER_NOT_SHOWN)


def label_specific(flags, gate: str) -> str:
    invalid, passed = _count(flags)
    if invalid > INVALID_MAX:
        return specific_name(gate, "unresolved")
    if passed >= SHOWN_MIN:
        return specific_name(gate, "replicated")
    return specific_name(gate, "not")


def label_advantage(flags) -> str:
    return eight_label(flags, ADVANTAGE_OBSERVED, ADVANTAGE_NOT)


def label_rival_afit(flags) -> str:
    return eight_label(flags, RIVAL_AFIT, RIVAL_AFIT_NOT)


def label_variation(specific: str, flags, gate: str) -> str:
    if specific != specific_name(gate, "replicated"):
        return VARIATION_FAIL
    invalid, passed = _count(flags)
    if invalid > INVALID_MAX or passed < SHOWN_MIN:
        return VARIATION_FAIL
    return VARIATION_OK


def _matrix_phrase(gates: list[str]) -> str:
    names = ["W_h%s" % gate for gate in gates]
    if len(names) == 1:
        return "The specified matrix is %s." % names[0]
    return "The specified matrices are %s." % ", ".join(names)


def assemble_claim(
    e1: str,
    transfer: str,
    specific: dict,
    variation: dict,
    advantage: str,
    rival_afit: str,
    rival_afit_count: int,
) -> str:
    """Exact claim wording, with rival and variation sentences appended."""
    replicated = [gate for gate in ("r", "z", "n") if specific[gate] == specific_name(gate, "replicated")]
    unresolved = [gate for gate in ("r", "z", "n") if specific[gate] == specific_name(gate, "unresolved")]
    rival_line = "Tuned-rival results: %s. %s (%d/10)." % (advantage, rival_afit, rival_afit_count)
    variation_line = "Variation results: " + "; ".join(
        "%s: %s" % (gate, variation[gate]) for gate in ("r", "z", "n")
    )
    descriptive = ""
    if e1 != E1_REPLICATED:
        descriptive = " Sections 4-6 are descriptive because E1 was not replicated."
    if e1 == E1_REPLICATED and transfer == TRANSFER_SHOWN and replicated:
        body = CLAIM_SUCCESS + " " + _matrix_phrase(replicated)
    elif e1 == E1_REPLICATED and transfer == TRANSFER_SHOWN:
        if unresolved and len(unresolved) == 3:
            reversion = CLAIM_REVERSION_UNRESOLVED + "."
        elif unresolved:
            reversion = (
                CLAIM_REVERSION_UNRESOLVED
                + " for "
                + ", ".join(unresolved)
                + ". "
                + CLAIM_REVERSION_FAIL
                + " among the remaining matrices."
            )
        else:
            reversion = CLAIM_REVERSION_FAIL + "."
        body = CLAIM_FIRST_SENTENCE + " " + reversion
    else:
        lines = [Q7_TRANSFER, Q7_TUNED, Q7_REVERSION + "."]
        if transfer == UNRESOLVED or e1 != E1_REPLICATED:
            lines.insert(0, E1_UNRESOLVED + "." if e1 != E1_REPLICATED else UNRESOLVED + ".")
        body = " ".join(lines)
    return body + descriptive + " " + rival_line + " " + variation_line
