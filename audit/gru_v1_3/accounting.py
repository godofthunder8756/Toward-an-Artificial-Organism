"""Claim-unit accounting. Unresolved and unfinished are never below-floor."""

from __future__ import annotations

TRAINED_ARMS = {
    7: (
        "cand_final",
        "f_init",
        "f_trained",
        "f_tuned32",
        "r_tuned843",
        "sel_g0.5_b-2.0",
        "sel_g0.5_b0.0",
        "sel_g0.5_b2.0",
        "sel_g1.0_b-2.0",
        "sel_g1.0_b0.0",
        "sel_g1.0_b2.0",
        "sel_g2.0_b-2.0",
        "sel_g2.0_b0.0",
        "sel_g2.0_b2.0",
    ),
    8: ("cand_final", "f_init", "f_trained"),
    9: ("cand_final", "f_init", "f_trained"),
    10: ("CAND", "R-FIX-32", "R-FIX-48"),
}


def quota_status(m: int, b: int, x: int, u: int, i: int) -> str:
    verified = m + b + x
    if verified < 8:
        return "UNRESOLVED (insufficient verified checkpoints)"
    if m >= 8:
        return "quota is attained"
    if m + u + i < 8:
        return "quota is not attained"
    return "quota attainment is UNRESOLVED"


def empty_counts():
    return {"m": 0, "b": 0, "x": 0, "u": 0, "i": 0}


def add_label(counts: dict, kind: str) -> None:
    key = {"meets-floor": "m", "below-floor": "b", "BOUNDARY": "x", "UNRESOLVED": "u", "INCOMPLETE": "i"}[kind]
    counts[key] += 1


def binomial_arithmetic() -> dict:
    # C(10,8)+C(10,9)+C(10,10) = 56, over 2^10. Arithmetic only, not a p-value.
    return {
        "numerator": 56,
        "denominator": 1024,
        "statement": (
            "56/1024 is reported only as arithmetic under ten independent fair "
            "Bernoulli trials and is not a p-value."
        ),
    }
