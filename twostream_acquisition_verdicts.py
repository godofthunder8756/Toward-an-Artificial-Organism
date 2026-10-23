"""Verdict rules for E1, E2, E3, and the assembled claim.

The label strings and the numerical cuts are the protocol's. This module does
not train and does not read network output; callers pass per-seed records.
"""

from __future__ import annotations

from twostream_acquisition_spec import (
    BASE_CLAIM,
    E1_NOT_SHOWN,
    E1_SHOWN,
    E1_UNRESOLVED,
    E2_FROZEN,
    E2_FROZEN_APPEND,
    E2_SUPPORTED,
    E2_SUPPORTED_APPEND,
    E2_UNCLEAR,
    E2_UNRESOLVED,
    E3_LOCALIZED,
    E3_LOCALIZED_APPEND,
    E3_NOT_LOCALIZED,
    E3_QUALIFIER,
    E3_UNRESOLVED,
    LABEL_CHART_ACCESSIBLE,
    LABEL_FROZEN_READOUT,
    LABEL_GENERALIZATION_WEAK,
    LABEL_TWO_DIMENSIONAL,
    NOT_SHOWN_MAX,
    PERMITTED_JOINT,
    REJECT_SENTENCE,
    SHOWN_MIN,
    STUDY_ADMIT,
    STUDY_REJECT,
    STUDY_UNRESOLVED,
)


def _count(records, predicate) -> int:
    return sum(1 for record in records if predicate(record))


def e1_label(records):
    """Primary GRU-8 CAND records with keys afit, alearn, integrity."""
    if len(records) != 10:
        return E1_UNRESOLVED
    n_conjunction = _count(
        records, lambda r: r["afit"] and r["alearn"] and r["integrity"]
    )
    n_afit = _count(records, lambda r: bool(r["afit"]))
    n_integrity = _count(records, lambda r: bool(r["integrity"]))
    if n_conjunction >= SHOWN_MIN:
        return E1_SHOWN
    if n_afit <= NOT_SHOWN_MAX and n_integrity >= SHOWN_MIN:
        return E1_NOT_SHOWN
    return E1_UNRESOLVED


def e2_label(records):
    """GRU-8 paired records.

    Keys: intact (both runs), tie (K-FR total excess at or below 1e-12),
    ratio_le_half, kfr_afit.
    """
    if len(records) != 10:
        return E2_UNRESOLVED
    n_ratio = _count(
        records,
        lambda r: r["intact"] and (not r["tie"]) and r["ratio_le_half"],
    )
    n_kfr_afit = _count(records, lambda r: bool(r["kfr_afit"]))
    if n_ratio >= SHOWN_MIN:
        return E2_SUPPORTED
    if n_kfr_afit >= SHOWN_MIN and n_ratio <= NOT_SHOWN_MAX:
        return E2_FROZEN
    if n_kfr_afit <= NOT_SHOWN_MAX and n_ratio <= NOT_SHOWN_MAX:
        return E2_UNCLEAR
    return E2_UNRESOLVED


def e3_label(records):
    """GRU-8 CAND records with localized, coverage_ok, rank_ok.

    Coverage or rank failure on any seed makes the study label UNRESOLVED
    rather than NOT LOCALIZED.
    """
    if len(records) != 10:
        return E3_UNRESOLVED
    if any((not r["coverage_ok"]) or (not r["rank_ok"]) for r in records):
        return E3_UNRESOLVED
    n_localized = _count(records, lambda r: bool(r["localized"]))
    if n_localized >= SHOWN_MIN:
        return E3_LOCALIZED
    if n_localized <= NOT_SHOWN_MAX:
        return E3_NOT_LOCALIZED
    return E3_UNRESOLVED


def kfr_e3_label(records):
    """Same rule as e3_label, applied to the matched K-FR runs."""
    return e3_label(records)


def e3_qualifier(kfr_records) -> bool:
    return kfr_e3_label(kfr_records) == E3_NOT_LOCALIZED


def study_verdict(e1: str, integrity_count: int) -> str:
    if integrity_count < SHOWN_MIN:
        return STUDY_UNRESOLVED
    if e1 == E1_SHOWN:
        return STUDY_ADMIT
    if e1 == E1_NOT_SHOWN:
        return STUDY_REJECT
    return STUDY_UNRESOLVED


def observation_labels(facts: dict) -> list[str]:
    """facts uses already-counted booleans. Labels are appended verbatim."""
    fired = []
    if facts.get("k2d_afit_at_least_8") or facts.get("k2dmlp_afit_at_least_8"):
        fired.append(LABEL_TWO_DIMENSIONAL)
    if facts.get("kfr_afit_at_least_8"):
        fired.append(LABEL_FROZEN_READOUT)
    if facts.get("generalization_weak"):
        fired.append(LABEL_GENERALIZATION_WEAK)
    if facts.get("chart_accessible"):
        fired.append(LABEL_CHART_ACCESSIBLE)
    return fired


def assemble_claim(verdict: str, e2: str, e3: str, qualifier: bool, labels: list[str]) -> str:
    """Claim ceiling text. The ADMIT base is stated only when the verdict is ADMIT."""
    if verdict == STUDY_REJECT:
        return REJECT_SENTENCE
    if verdict != STUDY_ADMIT:
        return "UNRESOLVED. The prespecified base claim is not made."
    parts = [BASE_CLAIM]
    if e2 == E2_FROZEN:
        parts.append(E2_FROZEN_APPEND)
    elif e2 == E2_SUPPORTED:
        parts.append(E2_SUPPORTED_APPEND)
    if e3 == E3_LOCALIZED:
        sentence = E3_LOCALIZED_APPEND
        if qualifier:
            sentence += " (" + E3_QUALIFIER + ")"
        parts.append(sentence)
    if e2 == E2_SUPPORTED and e3 == E3_LOCALIZED:
        parts.append(PERMITTED_JOINT)
    for label in labels:
        parts.append(label)
    return " ".join(parts)
