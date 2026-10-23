"""Stage S7. Pool stored losses and assign labels. No new finite-identity check."""

from __future__ import annotations

import math

from ckappa_oracle.pinned import FROZEN_RUNTIME, fnum
from ckappa_classfit.classes import CLASS_ORDER, GROUPS
from ckappa_classfit.pinned import INADMISSIBLE_CANDIDATES, SYSTEM_ORDER
from ckappa_classfit.rankcats import category_blocks_propagation
from ckappa_classfit.schedule import POOLED

REL = fnum("boundary_relative")
COVERAGE = fnum("coverage_fraction")
REFERENCE_EPS = FROZEN_RUNTIME["reference_eps_syn"]
EPS = tuple(FROZEN_RUNTIME["eps_syn"])
FIT_TYPES = ("global", "class")
LABEL_GROUPS = ("ALL", "MARG")
HEADROOM = {
    "ALL": {"sqrt_H": fnum("all_sqrt_H"), "R": fnum("all_R"), "met_label": "MET"},
    "MARG": {"sqrt_H": fnum("marg_sqrt_H"), "R": fnum("marg_R"), "met_label": "MET"},
}
IDENTITY_SYSTEMS = ("SYS-O6", "SYS-PC", "SYS-FK")
REPORTED_SYSTEMS = ("SYS-NC1", "SYS-NC2", "SYS-NC3", "SYS-LIM")


def _clearly_below(value: float, threshold: float) -> bool:
    return value < threshold * (1.0 - REL)


def _in_band(value: float, threshold: float) -> bool:
    return abs(value - threshold) <= REL * threshold


def _blank_pool(system, fit_type, group, eps, mode, reason: str) -> dict:
    return {
        "system": system,
        "fit_type": fit_type,
        "group": group,
        "eps_syn": eps,
        "mode": mode,
        "L_mu": None,
        "L_full": None,
        "S": None,
        "gain": None,
        "R": None,
        "sqrt_H": None,
        "n_scoreable": None,
        "law_mass": None,
        "formed": False,
        "not_formed_reason": reason,
    }


def _unformed_reason(system: dict | None, fit_type: str) -> str:
    if system is None or "maps" not in system:
        return "NOT_REACHED"
    blocked_empty = False
    blocked_unresolved = False
    for fold, slots in system["maps"].items():
        keys = ("global",) if fit_type == "global" else CLASS_ORDER
        # The common mask uses all four maps, so either fit type is blocked by any of them.
        for key in ("global",) + CLASS_ORDER:
            slot = slots[key]
            for category in (slot["full_category"], slot["mu_category"]):
                if category == "UNAVAILABLE_EMPTY":
                    blocked_empty = True
                elif category == "UNRESOLVED":
                    blocked_unresolved = True
        del fold, keys
    if blocked_unresolved:
        return "REFERENCE RANK UNRESOLVED"
    if blocked_empty:
        return "UNAVAILABLE"
    return "NOT_FORMED"


def _denominator(row: dict, mode: str) -> float:
    if mode == "weighted":
        mass = row.get("law_mass_scoreable")
        return 0.0 if mass is None else float(mass)
    count = row.get("n_scoreable")
    return 0.0 if count is None else float(count)


def pool_records(system_name: str, system: dict | None, records: list, admissible: bool) -> list:
    rows = []
    if not admissible:
        reason = "RESTRICTED COMPARATOR NOT ADMISSIBLE"
        for fit_type in FIT_TYPES:
            for group in GROUPS:
                for eps in EPS:
                    for mode in ("weighted", "unweighted"):
                        rows.append(_blank_pool(system_name, fit_type, group, eps, mode, reason))
        return rows
    for fit_type in FIT_TYPES:
        for group in GROUPS:
            for eps in EPS:
                for mode in ("weighted", "unweighted"):
                    chosen = [
                        row
                        for row in records
                        if row.get("fit_type") == fit_type
                        and row.get("group") == group
                        and row.get("eps_syn") == eps
                        and row.get("mode") == mode
                    ]
                    if not chosen or any(row.get("n_scoreable") is None for row in chosen):
                        rows.append(_blank_pool(system_name, fit_type, group, eps, mode, _unformed_reason(system, fit_type)))
                        continue
                    numerator_mu = 0.0
                    numerator_full = 0.0
                    numerator_s = 0.0
                    denominator = 0.0
                    n_score = 0
                    law_mass = 0.0
                    for row in chosen:
                        width = _denominator(row, mode)
                        n_score += int(row["n_scoreable"])
                        if row.get("law_mass_scoreable") is not None:
                            law_mass += float(row["law_mass_scoreable"])
                        if width == 0.0 or row.get("L_mu") is None:
                            continue
                        numerator_mu += float(row["L_mu"]) * width
                        numerator_full += float(row["L_full"]) * width
                        numerator_s += float(row["S"]) * width
                        denominator += width
                    if denominator == 0.0:
                        rows.append(_blank_pool(system_name, fit_type, group, eps, mode, "NOT_EVALUATED"))
                        continue
                    loss_mu = numerator_mu / denominator
                    loss_full = numerator_full / denominator
                    response = numerator_s / denominator
                    ratio = None if response == 0.0 else loss_mu / response
                    sqrt_h = math.sqrt(loss_mu) if loss_mu >= 0.0 else None
                    rows.append(
                        {
                            "system": system_name,
                            "fit_type": fit_type,
                            "group": group,
                            "eps_syn": eps,
                            "mode": mode,
                            "L_mu": loss_mu,
                            "L_full": loss_full,
                            "S": response,
                            "gain": loss_mu - loss_full,
                            "R": ratio,
                            "sqrt_H": sqrt_h,
                            "n_scoreable": n_score,
                            "law_mass": law_mass,
                            "formed": True,
                            "not_formed_reason": None,
                        }
                    )
    return rows


def _coverage_failure(rows: list, fit_type: str) -> bool:
    """True when a declared reference-size cell is absent or fails the 75% rules.

    An empty list is a failure only because the declared cells are absent.
    Callers that already know the system was inadmissible do not use this
    for that system's label (CI-LABEL-INADMISSIBLE).
    """
    expected = 6 if fit_type == "global" else 24
    relevant = []
    for row in rows:
        if row.get("eps_syn") != REFERENCE_EPS:
            continue
        if fit_type == "global" and row.get("class") is None:
            relevant.append(row)
        if fit_type == "class" and row.get("class") is not None:
            relevant.append(row)
    if len(relevant) < expected:
        return True
    for row in relevant:
        if 4 * int(row["n_scoreable"]) < 3 * int(row["n_total"]):
            return True
        mass_t = float(row["law_mass_total"])
        if mass_t == 0.0 or _clearly_below(float(row["law_mass_scoreable"]) / mass_t, COVERAGE):
            return True
    return False


def _identity_rows(system: dict | None, evaluation: dict | None) -> list:
    rows = []
    if system is not None:
        rows.extend(system.get("matrix_identities") or [])
    if evaluation is not None:
        rows.extend(evaluation.get("identities") or [])
    return rows


def _required_identities(system_name: str, fit_type: str, group: str, rows: list) -> list:
    if system_name not in IDENTITY_SYSTEMS:
        return []
    chosen = []
    for row in rows:
        # RL-3. D6 stays out of label identity_status. INVESTIGATE is D7 only.
        if str(row.get("identity_id", "")).startswith("D6") or str(row.get("identity_id", "")).startswith("D7"):
            continue
        if row.get("kind") == "diagnostic":
            continue
        if row.get("fit_type") != fit_type:
            continue
        row_group = row.get("group")
        if row_group not in (None, group):
            continue
        chosen.append(row)
    return chosen


def _identity_label(rows: list) -> tuple[str, str | None]:
    if not rows:
        return "NOT EVALUATED", "no identity record"
    if any(row.get("status") == "NOT_EVALUATED" for row in rows):
        return "NOT EVALUATED", "empty identity domain"
    if any(row.get("status") in ("REFERENCE_RANK_UNRESOLVED", "UNAVAILABLE") for row in rows):
        return "REFERENCE RANK UNRESOLVED", "required identity rank"
    if any(row.get("status") == "NOT_APPLICABLE_RANK" for row in rows):
        return "EXPECTATION NOT APPLICABLE (RANK)", "resolved lower rank"
    if any(row.get("status") == "FAIL" for row in rows):
        return "PIPELINE INVALID", "stored identity failure"
    if all(row.get("status") == "PASS" for row in rows):
        return "IDENTITY AS DERIVED", None
    return "NOT EVALUATED", "identity status outside the declared set"


def _rank_blocks(system: dict | None) -> str | None:
    if system is None or "maps" not in system:
        return "NOT_REACHED"
    empty = False
    unresolved = False
    for slots in system["maps"].values():
        for key in ("global",) + CLASS_ORDER:
            slot = slots[key]
            for category in (slot["full_category"], slot["mu_category"]):
                if category_blocks_propagation(category):
                    if category == "UNRESOLVED":
                        unresolved = True
                    else:
                        empty = True
    if unresolved:
        return "REFERENCE RANK UNRESOLVED"
    if empty:
        return "UNAVAILABLE"
    return None


def _flags(system_name, system, evaluation, fit_type, group, identities) -> dict:
    coverage = []
    crossings = 0
    if evaluation is not None:
        crossings = evaluation.get("crossings", 0)
        for row in evaluation.get("coverage") or []:
            if row.get("eps_syn") == REFERENCE_EPS:
                coverage.append(
                    {
                        "fold": row.get("fold"),
                        "class": row.get("class"),
                        "count_rule_pass": row.get("count_rule_pass"),
                        "mass_rule_pass": row.get("mass_rule_pass"),
                        "crossings": row.get("crossings"),
                    }
                )
    ranks = []
    if system is not None and "maps" in system:
        for fold, slots in system["maps"].items():
            keys = ("global",) if fit_type == "global" else CLASS_ORDER
            for key in keys:
                slot = slots[key]
                ranks.append(
                    {
                        "fold": fold,
                        "class": None if key == "global" else key,
                        "full_category": slot.get("full_category"),
                        "mu_category": slot.get("mu_category"),
                    }
                )
    return {
        "admissible": None if system is None else bool(system.get("admissible")),
        "voided_prefixes": [] if system is None else sorted(system.get("voids") or []),
        "crossings": crossings,
        "coverage_at_reference_eps": coverage,
        "rank": ranks,
        "identity_status": [
            {"identity_id": row.get("identity_id"), "status": row.get("status"), "group": row.get("group")}
            for row in identities
        ],
        "group": group,
        "system": system_name,
    }


def label_rows(systems: dict, evaluations: dict, stop_kind: str | None) -> list:
    rows = []
    for system_name in SYSTEM_ORDER:
        system = systems.get(system_name)
        evaluation = evaluations.get(system_name)
        identities = _identity_rows(system, evaluation)
        admissible = bool(system and system.get("admissible"))
        for fit_type in FIT_TYPES:
            for group in LABEL_GROUPS:
                required = _required_identities(system_name, fit_type, group, identities)
                flags = _flags(system_name, system, evaluation, fit_type, group, required)
                label, reason = _one_label(
                    system_name, system, evaluation, fit_type, group, required, admissible, stop_kind
                )
                rows.append(
                    {
                        "system": system_name,
                        "fit_type": fit_type,
                        "group": group,
                        "eps_syn": REFERENCE_EPS,
                        "label": label,
                        "first_failing_reason": reason,
                        "flags": flags,
                    }
                )
    return rows


def _one_label(system_name, system, evaluation, fit_type, group, required, admissible, stop_kind) -> tuple[str, str | None]:
    if stop_kind == "PIPELINE INVALID":
        return "PIPELINE INVALID", "operational failure diagnosis"
    if stop_kind in ("CAP REACHED", "CAP RESERVE REACHED", "PROJECTION HALT"):
        return stop_kind, "incomplete"
    if stop_kind not in (None, "COMPLETED"):
        return "NOT EVALUATED", stop_kind
    if system_name in INADMISSIBLE_CANDIDATES and not admissible:
        # No coverage row exists, so C7.1 item 3's "some fold" does not fire.
        return "RESTRICTED COMPARATOR NOT ADMISSIBLE", "stage S3 admissibility"
    if evaluation is None or system is None:
        return "NOT EVALUATED", "system evaluation was not stored"
    if _coverage_failure(evaluation.get("coverage") or [], fit_type):
        return "REFERENCE COVERAGE NOT MET", "count or law-mass coverage"
    blocked = _rank_blocks(system)
    if blocked is not None:
        return blocked, "required map"
    pooled_s = _reference_s(evaluation, fit_type, group)
    if pooled_s == 0.0:
        return "ZERO RESPONSE", "pooled S is exactly 0"
    if system_name in IDENTITY_SYSTEMS:
        return _identity_label(required)
    if system_name in REPORTED_SYSTEMS:
        return "REPORTED", None
    return "REPORTED", None


def _reference_s(evaluation: dict, fit_type: str, group: str):
    """Return pooled S at the reference size, or None when the pool is not formed."""
    records = [
        row
        for row in evaluation.get("loss_records") or []
        if row.get("fit_type") == fit_type and row.get("group") == group and row.get("eps_syn") == REFERENCE_EPS and row.get("mode") == "weighted"
    ]
    if not records or any(row.get("n_scoreable") is None or row.get("S") is None for row in records):
        return None
    numerator = 0.0
    denominator = 0.0
    for row in records:
        width = _denominator(row, "weighted")
        if width == 0.0:
            continue
        numerator += float(row["S"]) * width
        denominator += width
    if denominator == 0.0:
        return None
    return numerator / denominator


def _validation(systems, evaluations, stop_kind: str | None) -> dict:
    if stop_kind == "PIPELINE INVALID":
        return {"label": "CLASS-FIT VALIDATION NOT MET (PIPELINE INVALID)", "met": False, "first_failing_reason": "PIPELINE INVALID"}
    if stop_kind in ("CAP REACHED", "CAP RESERVE REACHED", "PROJECTION HALT"):
        return {"label": "CLASS-FIT VALIDATION NOT MET (INCOMPLETE)", "met": False, "first_failing_reason": stop_kind}
    if stop_kind not in (None, "COMPLETED"):
        return {"label": "CLASS-FIT VALIDATION NOT MET (NOT EVALUATED)", "met": False, "first_failing_reason": stop_kind}
    for system_name in IDENTITY_SYSTEMS:
        system = systems.get(system_name)
        evaluation = evaluations.get(system_name)
        rows = _identity_rows(system, evaluation)
        for fit_type in FIT_TYPES:
            required = _required_identities(system_name, fit_type, "ALL", rows)
            # Group-specific zero-gain rows are included by scanning every label group.
            for group in LABEL_GROUPS:
                required.extend(
                    row
                    for row in _required_identities(system_name, fit_type, group, rows)
                    if row.get("group") == group
                )
            seen = []
            keys = set()
            for row in required:
                key = row.get("identity_id")
                if key in keys:
                    continue
                keys.add(key)
                seen.append(row)
            label, reason = _identity_label(seen)
            if label == "NOT EVALUATED":
                return {
                    "label": "CLASS-FIT VALIDATION NOT MET (NOT EVALUATED)",
                    "met": False,
                    "first_failing_reason": "NOT EVALUATED",
                    "system": system_name,
                    "fit_type": fit_type,
                    "detail": reason,
                }
            if label == "EXPECTATION NOT APPLICABLE (RANK)":
                return {
                    "label": "CLASS-FIT VALIDATION NOT MET (RANK)",
                    "met": False,
                    "first_failing_reason": "RANK",
                    "system": system_name,
                    "fit_type": fit_type,
                }
            if label == "REFERENCE RANK UNRESOLVED":
                return {
                    "label": "CLASS-FIT VALIDATION NOT MET (REFERENCE RANK UNRESOLVED)",
                    "met": False,
                    "first_failing_reason": "REFERENCE RANK UNRESOLVED",
                    "system": system_name,
                    "fit_type": fit_type,
                }
            if label != "IDENTITY AS DERIVED":
                return {
                    "label": f"CLASS-FIT VALIDATION NOT MET ({label})",
                    "met": False,
                    "first_failing_reason": label,
                    "system": system_name,
                    "fit_type": fit_type,
                }
    return {"label": "CLASS-FIT VALIDATION MET", "met": True, "first_failing_reason": None}


def _headroom_one(group: str, pooled_row: dict | None, validation: dict, coverage_ok: bool, maps_ok: str | None) -> dict:
    thresholds = HEADROOM[group]
    base = {"group": group, "eps_syn": REFERENCE_EPS, "H_definition": "L_mu of the SYS-PC class fit at eps_syn 0.1"}
    if not validation.get("met"):
        return {**base, "label": "NOT FORMED (VALIDATION NOT MET)", "met": False}
    if maps_ok == "REFERENCE RANK UNRESOLVED":
        return {**base, "label": "REFERENCE RANK UNRESOLVED", "met": False}
    if maps_ok == "UNAVAILABLE":
        return {**base, "label": "UNAVAILABLE", "met": False}
    if not coverage_ok:
        return {**base, "label": "REFERENCE COVERAGE NOT MET", "met": False}
    if pooled_row is None or not pooled_row.get("formed"):
        reason = None if pooled_row is None else pooled_row.get("not_formed_reason")
        if reason == "NOT_EVALUATED":
            return {**base, "label": "NOT EVALUATED", "met": False}
        return {**base, "label": "ZERO RESPONSE", "met": False}
    response = pooled_row.get("S")
    loss_mu = pooled_row.get("L_mu")
    if response is None or loss_mu is None or pooled_row.get("n_scoreable") in (None, 0):
        return {**base, "label": "NOT EVALUATED", "met": False}
    if float(response) == 0.0:
        return {**base, "label": "ZERO RESPONSE", "met": False, "S": 0.0, "H": loss_mu}
    sqrt_h = math.sqrt(float(loss_mu))
    ratio = float(loss_mu) / float(response)
    values = {
        "H": loss_mu,
        "S": response,
        "sqrt_H": sqrt_h,
        "sqrt_H_threshold": thresholds["sqrt_H"],
        "R": ratio,
        "R_definition": "comparator squared prediction error divided by actual response energy",
        "R_threshold": thresholds["R"],
    }
    clear = []
    band = []
    if _clearly_below(sqrt_h, thresholds["sqrt_H"]):
        clear.append("sqrt_H")
    if _clearly_below(ratio, thresholds["R"]):
        clear.append("R")
    if _in_band(sqrt_h, thresholds["sqrt_H"]):
        band.append("sqrt_H")
    if _in_band(ratio, thresholds["R"]):
        band.append("R")
    if clear:
        return {**base, "label": "HEADROOM NOT MET", "met": False, "values": values, "clearly_below": clear}
    if band:
        return {**base, "label": "BOUNDARY", "met": False, "values": values, "boundary": band}
    return {**base, "label": thresholds["met_label"], "met": True, "values": values}


def headroom(systems, evaluations, pooled, validation: dict) -> dict:
    system = systems.get("SYS-PC")
    evaluation = evaluations.get("SYS-PC")
    maps_ok = _rank_blocks(system)
    coverage_ok = evaluation is not None and not _coverage_failure(evaluation.get("coverage") or [], "class")
    out = {}
    for group in LABEL_GROUPS:
        row = None
        for candidate in pooled:
            if (
                candidate["system"] == "SYS-PC"
                and candidate["fit_type"] == "class"
                and candidate["group"] == group
                and candidate["eps_syn"] == REFERENCE_EPS
                and candidate["mode"] == "weighted"
            ):
                row = candidate
                break
        out[group] = _headroom_one(group, row, validation, coverage_ok, maps_ok)
    return out


def d7_flags(systems: dict) -> list:
    system = systems.get("SYS-LIM") or {}
    found = []
    for row in system.get("matrix_identities") or []:
        if str(row.get("identity_id", "")).startswith("D7") and row.get("status") == "INVESTIGATE":
            found.append(
                {
                    "identity_id": row.get("identity_id"),
                    "status": "INVESTIGATE",
                    "role": "non-stopping; outside VALIDATION and HEADROOM",
                }
            )
    return found


def stage_s7(run, ctx, stop_kind: str | None) -> dict:
    run.check_deadline("S7")
    systems = ctx.get("systems") or {}
    evaluations = ctx.get("evaluations") or {}
    pooled = []
    for system_name in SYSTEM_ORDER:
        system = systems.get(system_name)
        evaluation = evaluations.get(system_name) or {}
        admissible = bool(system and system.get("admissible"))
        pooled.extend(pool_records(system_name, system, evaluation.get("loss_records") or [], admissible))
    if len(pooled) != POOLED:
        from ckappa_oracle.io import integrity_stop

        integrity_stop("pooled aggregate count drifted", found=len(pooled), expected=POOLED)
    labels = label_rows(systems, evaluations, stop_kind if stop_kind != "COMPLETED" else None)
    validation = _validation(systems, evaluations, None if stop_kind == "COMPLETED" else stop_kind)
    room = headroom(systems, evaluations, pooled, validation)
    investigate = d7_flags(systems)
    return {
        "pooled": pooled,
        "labels": labels,
        "VALIDATION": validation,
        "HEADROOM": room,
        "d7_investigate": investigate,
    }
