"""Stage S4. Applicable P0 checks after the L and G tables exist (C4.0, E39-2)."""

from __future__ import annotations

import numpy as np

from ckappa_oracle.io import integrity_stop
from ckappa_classfit.classes import FLIPS
from ckappa_classfit.rankcats import comparison_tolerance
from ckappa_classfit.records import diag3, max_abs

R_MAT = {
    "X": diag3(-1.0, 1.0, -1.0),
    "Y": diag3(1.0, -1.0, -1.0),
    "XY": diag3(-1.0, -1.0, 1.0),
}
P_MAT = R_MAT


def _stop(reason: str, **detail):
    """RL-8. P0 failure is INTEGRITY STOP, exit 7, with the check named."""
    integrity_stop("PIPELINE INVALID (P0)", diagnosis="PIPELINE INVALID (P0)", check=reason, **detail)


def _pair_ok(left: np.ndarray, right: np.ndarray) -> tuple[float, float, bool]:
    residual = max_abs(left - right)
    tolerance = comparison_tolerance(max_abs(left), max_abs(right))
    return residual, tolerance, residual <= tolerance


def stage_s4(run, ctx) -> dict:
    run.check_deadline("S4")
    systems = ctx["systems"]
    exact = ctx["P_h_exact"]
    law_rows = []
    law_domain = []
    for prefix in range(16):
        for name, mask in FLIPS:
            for continuation in range(16):
                image_prefix = prefix ^ mask
                image_u = continuation ^ mask
                law_domain.append({"a": prefix, "g": name, "u": continuation})
                equal = exact[(image_prefix, image_u)] == exact[(prefix, continuation)]
                law_rows.append(
                    {
                        "chart": "law",
                        "kind": "P_exact",
                        "a": prefix,
                        "g": name,
                        "u": continuation,
                        "residual_max_abs": 0.0 if equal else 1.0,
                        "tolerance": 0.0,
                        "pass": equal,
                    }
                )
                if not equal:
                    payload = _partial(law_rows, [], [], "FAIL", "law")
                    run.write_json("stage_S4_P0.json", payload)
                    _stop("P0 probability invariance", a=prefix, g=name, u=continuation)

    charts = [("true", systems["SYS-O6"])]
    charts.append(("SYS-FK", systems["SYS-FK"]))
    if systems["SYS-NC1"]["admissible"]:
        charts.append(("SYS-NC1", systems["SYS-NC1"]))

    comparisons = []
    omitted = []
    domains = {}
    # M-10 / E39-10. Record every applicability domain before any L or G comparison.
    for chart_name, system in charts:
        voids = system["voids"]
        domain = []
        for prefix in range(16):
            for gname, mask in FLIPS:
                image = prefix ^ mask
                reason = None
                if prefix in voids and image in voids:
                    reason = "VOID_both"
                elif prefix in voids:
                    reason = "VOID_a"
                elif image in voids:
                    reason = "VOID_ga"
                if reason is not None:
                    omitted.append({"chart": chart_name, "a": prefix, "g": gname, "reason": reason})
                    continue
                domain.append({"a": prefix, "g": gname})
        domains[chart_name] = domain
        system["p0_domain_pairs"] = domain
    # RL-13 / N-2. This write is not a verdict. PASS and FAIL come after comparisons.
    payload = _partial(law_rows, comparisons, omitted, "DOMAINS_RECORDED", None)
    payload["p0_domain_pairs"] = domains
    payload["domains_recorded_before_comparisons"] = True
    run.write_json("stage_S4_P0.json", payload)
    for chart_name, system in charts:
        voids = system["voids"]
        for prefix in range(16):
            for gname, mask in FLIPS:
                image = prefix ^ mask
                if prefix in voids or image in voids:
                    if chart_name == "true":
                        payload = _partial(law_rows, comparisons, omitted, "FAIL", chart_name)
                        payload["p0_domain_pairs"] = domains
                        payload["domains_recorded_before_comparisons"] = True
                        run.write_json("stage_S4_P0.json", payload)
                        integrity_stop(
                            "true-chart P0 pair omitted",
                            diagnosis="PIPELINE INVALID (P0)",
                            a=prefix,
                            g=gname,
                        )
                    continue
                rotation = R_MAT[gname]
                forecast_flip = P_MAT[gname]
                for continuation in range(16):
                    image_u = continuation ^ mask
                    left = system["L"][(image, image_u)]
                    right = forecast_flip @ system["L"][(prefix, continuation)] @ rotation
                    residual, tolerance, ok = _pair_ok(left, right)
                    comparisons.append(
                        {
                            "chart": chart_name,
                            "kind": "L",
                            "a": prefix,
                            "g": gname,
                            "u": continuation,
                            "residual_max_abs": residual,
                            "tolerance": tolerance,
                            "pass": ok,
                        }
                    )
                    if not ok:
                        failed = _partial(law_rows, comparisons, omitted, "FAIL", chart_name)
                        failed["p0_domain_pairs"] = domains
                        failed["domains_recorded_before_comparisons"] = True
                        run.write_json("stage_S4_P0.json", failed)
                        _stop("P0 L", chart=chart_name, a=prefix, g=gname, u=continuation, residual=residual, tolerance=tolerance)
                left_g = system["G"][image]
                right_g = rotation @ system["G"][prefix] @ rotation
                residual, tolerance, ok = _pair_ok(left_g, right_g)
                comparisons.append(
                    {
                        "chart": chart_name,
                        "kind": "G",
                        "a": prefix,
                        "g": gname,
                        "u": None,
                        "residual_max_abs": residual,
                        "tolerance": tolerance,
                        "pass": ok,
                    }
                )
                if not ok:
                    failed = _partial(law_rows, comparisons, omitted, "FAIL", chart_name)
                    failed["p0_domain_pairs"] = domains
                    failed["domains_recorded_before_comparisons"] = True
                    run.write_json("stage_S4_P0.json", failed)
                    _stop("P0 G", chart=chart_name, a=prefix, g=gname, residual=residual, tolerance=tolerance)

    payload = _partial(law_rows, comparisons, omitted, "PASS", None)
    payload["p0_domain_pairs"] = domains
    payload["domains_recorded_before_comparisons"] = True
    payload["memory"] = run.memory_observation()
    run.write_json("stage_S4_P0.json", payload)
    run.checkpoint("S4")
    run.log("stage S4 written")
    return payload


def _partial(law_rows, comparisons, omitted, status, failed_chart) -> dict:
    return {
        "stage": "S4",
        "status": status,
        "failed_chart": failed_chart,
        "law_domain_count": len(law_rows),
        "P_exact": law_rows,
        "comparisons": comparisons,
        "omitted_pairs": omitted,
    }
