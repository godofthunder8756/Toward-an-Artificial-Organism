"""Rank categories, B3 status, tolerances, and skip precedence.

Bands are the inherited closed interval [1e-10, 1e-6] (NOTE_1 N2, E39-8).
"""

from __future__ import annotations

from ckappa_oracle.io import integrity_stop

BAND_LO = 1e-10
BAND_HI = 1e-6
RCOND = 1e-10

TERMINAL_CATEGORIES = (
    "ATTEMPTED",
    "SKIPPED_PRIOR_STOP",
    "SKIPPED_SYSTEM_INADMISSIBLE",
    "SKIPPED_PREFIX_VOID",
    "SKIPPED_UNAVAILABLE_MAP",
    "UNKNOWN_AFTER_LAST_DURABLE",
)


def rank_category_from_ratios(ratios: list[float] | None, sigma_1: float | None, n_cols: int, empty: bool) -> str:
    """Literal NOTE_1 N2 / C3.3(a′) categories.

    ratios are sigma_i / sigma_1 for the singular values that exist.
    Full column rank requires n_cols ratios, each > 1e-6.
    """
    if empty:
        return "UNAVAILABLE_EMPTY"
    if sigma_1 is None:
        integrity_stop(
            "nonempty design missing sigma_1",
            diagnosis="PIPELINE INVALID (rank)",
        )
    if float(sigma_1) == 0.0:
        return "ZERO_NONEMPTY"
    if not ratios:
        return "ZERO_NONEMPTY"
    if any(BAND_LO <= float(value) <= BAND_HI for value in ratios):
        return "UNRESOLVED"
    resolved = sum(1 for value in ratios if float(value) > BAND_HI)
    if resolved == n_cols and len(ratios) >= n_cols:
        return "FULL"
    return "LOWER"


def category_is_full(category: str) -> bool:
    return category == "FULL"


def category_blocks_propagation(category: str) -> bool:
    """Empty and unresolved maps are not propagated. Lower rank and zero are."""
    return category in ("UNAVAILABLE_EMPTY", "UNRESOLVED")


def b3_status(sigma: list[float] | None, formed: bool) -> str:
    """C3.11(c)–(d) and RL-10.

    An unformed stack is NOT_FORMED and is not a stop. A formed stack with
    fewer than three singular values breaks the (48·n_fit)×8 shape invariant.
    That is INTEGRITY STOP, never PASS. A formed stack of the declared shape
    has eight singular values, so the short-stack stop is unreachable there.
    """
    if not formed or sigma is None:
        return "NOT_FORMED"
    # RL-13 / CNA note 1. A short formed stack stops before the ZERO return.
    if len(sigma) < 3:
        integrity_stop(
            "B3 stack has fewer than 3 singular values",
            diagnosis="PIPELINE INVALID (B3 short stack)",
            n_sigma=len(sigma),
            shape_invariant="(48*n_fit) x 8",
        )
    if float(sigma[0]) == 0.0:
        return "ZERO"
    sigma1 = float(sigma[0])
    third = float(sigma[2]) / sigma1
    if third > BAND_HI:
        return "RESOLVED_THIRD_DIRECTION"
    if BAND_LO <= third <= BAND_HI:
        return "UNRESOLVED-B3"
    return "PASS"


def comparison_tolerance(max_a: float, max_b: float) -> float:
    return 1e-12 + 1e-10 * max(max_a, max_b)


def cancellation_tolerance(scales: list[float]) -> float:
    return 1e-12 + 1e-10 * sum(scales)


def zero_gain_tolerance(response_energy: float) -> float:
    return 1e-18 + 1e-9 * response_energy


def recovery_ok(max_abs: float) -> bool:
    return max_abs <= 1e-9


def zero_gain_ok(loss_mu: float, loss_full: float, response_energy: float) -> bool:
    return abs(loss_mu - loss_full) <= zero_gain_tolerance(response_energy)


def skip_reason(
    *,
    stopped: bool,
    system_inadmissible: bool,
    prefix_void: bool,
    map_unavailable: bool,
) -> str | None:
    """First applicable unattempted reason. None means the call is attempted.

    Precedence (E39-7): prior stop, whole-system inadmissibility, prefix
    void, unavailable map.
    """
    if stopped:
        return "SKIPPED_PRIOR_STOP"
    if system_inadmissible:
        return "SKIPPED_SYSTEM_INADMISSIBLE"
    if prefix_void:
        return "SKIPPED_PREFIX_VOID"
    if map_unavailable:
        return "SKIPPED_UNAVAILABLE_MAP"
    return None
