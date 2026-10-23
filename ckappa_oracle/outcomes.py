"""N1 section-5 labels at eps_syn = 0.1. First match wins."""

from __future__ import annotations

import math

from ckappa_oracle.pinned import FROZEN_RUNTIME, fnum

REL = fnum("boundary_relative")
COVERAGE = fnum("coverage_fraction")
THRESHOLDS = {
    "ALL": {"sqrt_H": fnum("all_sqrt_H"), "R": fnum("all_R"), "met_label": "MET"},
    "MARG": {"sqrt_H": fnum("marg_sqrt_H"), "R": fnum("marg_R"), "met_label": "AVAILABLE"},
}


def _clearly_below(value: float, threshold: float) -> bool:
    return value < threshold * (1.0 - REL)


def _in_band(value: float, threshold: float) -> bool:
    return abs(value - threshold) <= REL * threshold


def classify_group(group: str, coverage_rows: list, any_rank_unresolved: bool, pooled: dict | None) -> dict:
    """coverage_rows are the resolved folds only. pooled is None when rank is unresolved."""
    thresholds = THRESHOLDS[group]
    count_failures = []
    mass_clear = []
    mass_band = []
    mass_values = []
    for row in coverage_rows:
        ratio_count = {
            "fold": row["fold"],
            "n_scoreable": row["n_scoreable"],
            "n_total": row["n_total"],
        }
        if 4 * row["n_scoreable"] < 3 * row["n_total"]:
            count_failures.append(ratio_count)
        mass = row["mass_coverage"]
        mass_values.append({"fold": row["fold"], "law_mass_coverage": mass})
        if _clearly_below(mass, COVERAGE):
            mass_clear.append({"fold": row["fold"], "law_mass_coverage": mass})
        if _in_band(mass, COVERAGE):
            mass_band.append({"fold": row["fold"], "law_mass_coverage": mass})
    if count_failures or mass_clear:
        return {
            "group": group,
            "eps_syn": FROZEN_RUNTIME["reference_eps_syn"],
            "label": "REFERENCE COVERAGE NOT MET",
            "reason": "a fold failed the integer 75% count test or its law-mass coverage is clearly below 0.75",
            "values": {
                "count_failures": count_failures,
                "law_mass_clearly_below": mass_clear,
                "law_mass": mass_values,
            },
        }
    if any_rank_unresolved:
        return {
            "group": group,
            "eps_syn": FROZEN_RUNTIME["reference_eps_syn"],
            "label": "REFERENCE RANK UNRESOLVED",
            "reason": "a fold design for B or B_mu is rank-unresolved; no pooled section 5 statistic is formed",
            "values": {"pooled_section5_statistic": "not_formed"},
        }
    if pooled is None:
        raise ValueError("pooled section 5 statistic is missing")
    response = pooled["S"]
    if response == 0.0:
        return {
            "group": group,
            "eps_syn": FROZEN_RUNTIME["reference_eps_syn"],
            "label": "ZERO RESPONSE",
            "reason": "pooled response energy S is exactly 0; R* is UNDEFINED",
            "values": {"S": 0.0, "H": pooled["H"], "R": "UNDEFINED", "sqrt_H": "UNDEFINED"},
        }
    sqrt_h = math.sqrt(pooled["H"])
    ratio = pooled["R"]
    headroom = {
        "sqrt_H": sqrt_h,
        "sqrt_H_threshold": thresholds["sqrt_H"],
        "R": ratio,
        "R_threshold": thresholds["R"],
        "H": pooled["H"],
        "S": response,
        "L_full": pooled["L_full"],
        "measured_gain": pooled["measured_gain"],
        "law_mass_in_boundary_band": mass_band,
    }
    clear = []
    band = list(mass_band)
    if _clearly_below(sqrt_h, thresholds["sqrt_H"]):
        clear.append("sqrt_H")
    if _clearly_below(ratio, thresholds["R"]):
        clear.append("R")
    if _in_band(sqrt_h, thresholds["sqrt_H"]):
        band.append({"statistic": "sqrt_H", "value": sqrt_h, "threshold": thresholds["sqrt_H"]})
    if _in_band(ratio, thresholds["R"]):
        band.append({"statistic": "R", "value": ratio, "threshold": thresholds["R"]})
    if clear:
        return {
            "group": group,
            "eps_syn": FROZEN_RUNTIME["reference_eps_syn"],
            "label": "HEADROOM NOT MET",
            "reason": "a float headroom statistic is clearly below its threshold",
            "values": {**headroom, "clearly_below": clear},
        }
    if band:
        return {
            "group": group,
            "eps_syn": FROZEN_RUNTIME["reference_eps_syn"],
            "label": "BOUNDARY",
            "reason": "no clear failure, and at least one float statistic lies in the boundary band",
            "values": {**headroom, "boundary": band},
        }
    return {
        "group": group,
        "eps_syn": FROZEN_RUNTIME["reference_eps_syn"],
        "label": thresholds["met_label"],
        "reason": "count coverage, law-mass coverage, sqrt(H*), and R* are all clearly met",
        "values": headroom,
    }
