"""Stage S3. System construction, before any intervention-response-map fit (E39-2)."""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction

import numpy as np

from ckappa_oracle.geometry import g_gradient, g_value, monomials, weighted_mean_and_sd
from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_oracle.linalg_fit import fit_from_svd
from ckappa_oracle.pinned import fnum
from ckappa_oracle.world import closed_form_L, fraction_text, inverse_chart_float
from ckappa_classfit.classes import CHI, CLASS_ORDER, ORBITS, class_of_prefix, declared_matches_xor, orbit_of_prefix
from ckappa_classfit.pinned import EXACT_T, FROZEN_RUNTIME, INADMISSIBLE_CANDIDATES, SYSTEM_ORDER, TRUE_CHART_SYSTEMS
from ckappa_classfit.rankcats import comparison_tolerance, rank_category_from_ratios
from ckappa_classfit.records import diag3, matrix_record, matrix_sha, max_abs

GUARD = fnum("guard")
EPS = tuple(FROZEN_RUNTIME["eps_syn"])


def _pipeline(reason: str, exit_code: int, **detail):
    payload = {"reason": reason}
    payload.update(detail)
    raise PackageStop("PIPELINE INVALID", exit_code, payload)


def _hash_sequence(matrices) -> str | None:
    if not matrices:
        return None
    digest = hashlib.sha256()
    for matrix in matrices:
        digest.update(np.ascontiguousarray(matrix, dtype="<f8").tobytes())
    return digest.hexdigest()


def _valid(belief: np.ndarray) -> bool:
    return bool(np.all(np.asarray(belief, dtype=np.float64) >= GUARD))


def _sign_pm(value: float) -> int:
    if value > 0.0:
        return 1
    if value < 0.0:
        return -1
    return 0


def _normalize(values: np.ndarray, weights: np.ndarray):
    mean, sd = weighted_mean_and_sd(np.asarray(values, dtype=np.float64), np.asarray(weights, dtype=np.float64))
    if np.any(sd == 0.0) or not np.all(np.isfinite(sd)) or not np.all(np.isfinite(mean)):
        integrity_stop("P-weighted chart standard deviation is 0")
    return mean, sd


def _embed_matrix(sd: np.ndarray, q_factor: np.ndarray) -> np.ndarray:
    """D @ Q.T, shape (k, 8)."""
    return np.diag(np.asarray(sd, dtype=np.float64)) @ np.asarray(q_factor, dtype=np.float64).T


def _sequential_sum(terms) -> float:
    total = 0.0
    for term in terms:
        total += float(term)
    return total


def _mark_inadmissible(run, system: str) -> None:
    """No subsequent response-map fits, B3 stacks, or evaluation propagations."""
    run.ledger.dump_remaining("SKIPPED_SYSTEM_INADMISSIBLE", system=system, stage="S5")
    run.ledger.dump_remaining("SKIPPED_SYSTEM_INADMISSIBLE", system=system, stage="S6", unit="propagation")


def _tables_for(run, ctx, system: str, baseline: np.ndarray, slope: dict, voids: set):
    """Closed-form L at non-voided baselines, then J = L @ slope and G, r."""
    if system in TRUE_CHART_SYSTEMS:
        ell = ctx["L_true"]
    else:
        ell = {}
        for prefix in range(16):
            if prefix in voids:
                continue
            for continuation in range(16):
                try:
                    ell[(prefix, continuation)] = closed_form_L(baseline[prefix], continuation, run.transition)
                except ValueError as exc:
                    integrity_stop("closed-form L failed", system=system, prefix=prefix, continuation=continuation, error=str(exc))
    jay = {}
    gee = {}
    arr = {}
    for prefix in range(16):
        if prefix in voids:
            continue
        gram = np.zeros((3, 3), dtype=np.float64)
        rhs = np.zeros((3, 8), dtype=np.float64)
        local_slope = slope[prefix]
        for continuation in range(16):
            local_l = ell[(prefix, continuation)]
            local_j = local_l @ local_slope
            jay[(prefix, continuation)] = local_j
            weight = float(ctx["P_h"][(prefix, continuation)])
            gram += weight * (local_l.T @ local_l)
            rhs += weight * (local_l.T @ local_j)
        gee[prefix] = gram
        arr[prefix] = rhs
    return ell, jay, gee, arr


def _table_hashes(ell, jay, gee, arr, voids: set) -> dict:
    ell_list = []
    jay_list = []
    gee_list = []
    arr_list = []
    for prefix in range(16):
        if prefix in voids:
            continue
        gee_list.append(gee[prefix])
        arr_list.append(arr[prefix])
        for continuation in range(16):
            ell_list.append(ell[(prefix, continuation)])
            jay_list.append(jay[(prefix, continuation)])
    return {
        "L_sha256": _hash_sequence(ell_list),
        "J_sha256": _hash_sequence(jay_list),
        "G_sha256": _hash_sequence(gee_list),
        "r_sha256": _hash_sequence(arr_list),
        "n_L": len(ell_list),
        "n_J": len(jay_list),
    }


def _void_report(baseline: np.ndarray) -> tuple[list, set]:
    rows = []
    voids = set()
    for prefix in range(16):
        belief = inverse_chart_float(baseline[prefix])
        if not _valid(belief):
            voids.add(prefix)
            rows.append(
                {
                    "prefix": prefix,
                    "label": "RESTRICTED COMPARATOR NOT ADMISSIBLE",
                    "min_p": float(np.min(belief)),
                }
            )
    return rows, voids


def _refit_nc1(run, ctx, committed: list) -> dict:
    design_rows = []
    target = []
    for prefix in range(16):
        mu_x = float(ctx["theta"][prefix, 0])
        mu_y = float(ctx["theta"][prefix, 1])
        kappa = float(ctx["theta"][prefix, 2])
        scale = math.sqrt(float(ctx["P_a"][prefix]))
        design_rows.append(scale * monomials(mu_x, mu_y))
        target.append(scale * kappa)
    run.note_svd()
    run.ledger.add("SYS-NC1", "S3", "fit", "ATTEMPTED", 1, "valid_finite")
    coef, report = fit_from_svd(np.vstack(design_rows), np.asarray(target, dtype=np.float64))
    category = rank_category_from_ratios(report.get("ratios"), report.get("sigma_1"), 6, False)
    if coef is None or category != "FULL":
        integrity_stop(
            "SYS-NC1 refit is not a resolved full-column coefficient vector",
            rank_category=category,
            sigma=report.get("sigma"),
        )
    coef = np.asarray(coef, dtype=np.float64).reshape(6)
    committed_vec = np.asarray(committed, dtype=np.float64)
    diff = max_abs(coef - committed_vec)
    tolerance = comparison_tolerance(max_abs(coef), max_abs(committed_vec))
    if diff > tolerance:
        integrity_stop(
            "SYS-NC1 refit mismatch",
            max_abs_diff=diff,
            tolerance=tolerance,
        )
    other = [float(coef[index]) for index in (0, 1, 2, 3, 5)]
    return {
        "coefficients": [float(value) for value in coef],
        "coef": coef,
        "committed_coefficients": [float(value) for value in committed_vec],
        "max_abs_diff": diff,
        "tolerance": tolerance,
        "rank_category": category,
        "sigma": report.get("sigma"),
        "sigma_1": report.get("sigma_1"),
        "ratios": report.get("ratios"),
        "n_inverted": report.get("n_inverted"),
        "n_rows": 16,
        "n_cols": 6,
        "exact_reduction_to_cross_term": all(value == 0.0 for value in other),
        "exact_reduction_note": "frozen exact-zero test on c0,c1,c2,c3,c5; not a tolerance check",
    }


def rho_nc1_exact_law(coef: np.ndarray, mu_x, mu_y, p_a_exact) -> dict:
    """RL-1. rho_NC1 from the refitted g on all 16 exact-law prefixes.

    This is a coefficient rule. SYS-NC1 prefix voiding and admissibility are
    not arguments, and E39-7's skip rule is not applied. The caller must not
    pass a void set, an admissibility flag, or the ledger.
    """
    mu_x_values = [float(value) for value in mu_x]
    mu_y_values = [float(value) for value in mu_y]
    weights = [Fraction(value) for value in p_a_exact]
    if len(mu_x_values) != 16 or len(mu_y_values) != 16 or len(weights) != 16:
        integrity_stop(
            "rho_NC1 requires all 16 exact-law prefixes",
            n_mu_x=len(mu_x_values),
            n_mu_y=len(mu_y_values),
            n_p=len(weights),
        )
    total = sum(weights, start=Fraction(0))
    if total != 1:
        _pipeline("normalization", 7, P_sum_exact=fraction_text(total))
    p_sum_float = float(total)
    p_float = [float(value) for value in weights]
    coef = np.asarray(coef, dtype=np.float64).reshape(6)
    rho_terms = []
    m4_terms = []
    for prefix in range(16):
        gradient = g_gradient(coef, mu_x_values[prefix], mu_y_values[prefix])
        rho_terms.append(p_float[prefix] * float(gradient @ gradient))
        m4_terms.append(p_float[prefix] * (mu_x_values[prefix] ** 4))
    rho_sq = _sequential_sum(rho_terms)
    m4 = _sequential_sum(m4_terms)
    if rho_sq < 0.0 or m4 <= 0.0 or p_sum_float <= 0.0:
        integrity_stop("RMS denominator is not positive", rho_sq=rho_sq, M4=m4, P_sum_float=p_sum_float)
    rho = math.sqrt(rho_sq)
    c2 = rho / math.sqrt(p_sum_float)
    c3 = rho / (3.0 * math.sqrt(m4))
    if not (c2 > 0.0 and c3 > 0.0):
        integrity_stop("RMS coefficients are not positive", c2=c2, c3=c3)
    return {
        "rho_NC1": rho,
        "M4": m4,
        "P_sum_float": p_sum_float,
        "c2": c2,
        "c3": c3,
        "summation_order": "sequential a=0..15",
        "P_a_float": p_float,
        "n_prefixes": 16,
        "prefix_domain": "exact-law a=0..15",
        "independent_of_sys_nc1_voids": True,
        "independent_of_sys_nc1_admissibility": True,
        "e39_7_skip_applied": False,
        "unit": "coefficient_rule",
    }


def _finish_system(run, ctx, name, baseline, slope, voids, mean, sd, extra):
    void_rows = extra.get("void_rows")
    if void_rows is None:
        void_rows, voids = _void_report(baseline)
    admissible = name not in INADMISSIBLE_CANDIDATES or (len(voids) < int(FROZEN_RUNTIME["o7_void_stop_count"]) and len(voids) == 0)
    # C7.1 item 5 ORs "≥5 voided" with "a matched baseline invalid".
    # A matched baseline invalid is a void, so one void is sufficient for NC systems.
    # CI-NC-ONE-VOID records the redundancy with the inherited ≥5 rule.
    if name in INADMISSIBLE_CANDIDATES and (len(voids) >= int(FROZEN_RUNTIME["o7_void_stop_count"]) or len(voids) > 0):
        admissible = False
    if name in TRUE_CHART_SYSTEMS and voids:
        integrity_stop("true-chart baseline voided", system=name, prefixes=sorted(voids))
    record = {
        "name": name,
        "admissible": admissible,
        "voided_prefixes": void_rows,
        "voids": voids,
        "baseline": baseline,
        "mean": mean,
        "sd": sd,
        "normalization": {
            "mean": matrix_record(np.asarray(mean, dtype=np.float64).reshape(1, -1)),
            "sd": matrix_record(np.asarray(sd, dtype=np.float64).reshape(1, -1)),
        },
    }
    record.update(extra)
    if not admissible:
        record["L"] = {}
        record["J"] = {}
        record["G"] = {}
        record["r"] = {}
        record["hashes"] = {"L_sha256": None, "J_sha256": None, "G_sha256": None, "r_sha256": None, "n_L": 0, "n_J": 0}
        _mark_inadmissible(run, name)
    else:
        ell, jay, gee, arr = _tables_for(run, ctx, name, baseline, slope, voids)
        record["L"] = ell
        record["J"] = jay
        record["G"] = gee
        record["r"] = arr
        record["slope"] = slope
        record["hashes"] = _table_hashes(ell, jay, gee, arr, voids)
    return record


def stage_s3(run, ctx, draws, committed_g: list) -> dict:
    run.check_deadline("S3")
    if not declared_matches_xor():
        integrity_stop("class XOR table does not match the declared C3.1 table")
    orbits = orbit_of_prefix()
    classes = class_of_prefix(orbits)
    ctx["orbit_of"] = orbits
    ctx["class_of"] = classes
    q_matrix = draws["Q"]
    q2 = draws["Q2"]
    systems = {}
    representative_positive = {}
    for orbit, prefix in (("A", 0), ("B", 1), ("C", 2), ("D", 3)):
        representative_positive[orbit] = bool(ctx["theta"][prefix, 0] > 0.0 and ctx["theta"][prefix, 1] > 0.0)

    # SYS-O6
    mean, sd = _normalize(ctx["theta"], ctx["P_a"])
    b_true = _embed_matrix(sd, q_matrix)
    slope = {prefix: b_true for prefix in range(16)}
    systems["SYS-O6"] = _finish_system(
        run, ctx, "SYS-O6", ctx["theta"].copy(), slope, set(), mean, sd,
        {"B_true": b_true, "chart": "true", "readout": "affine"},
    )

    # SYS-PC
    psi = np.zeros((16, 3), dtype=np.float64)
    for prefix in range(16):
        mu_x = float(ctx["theta"][prefix, 0])
        mu_y = float(ctx["theta"][prefix, 1])
        kappa = float(ctx["theta"][prefix, 2])
        psi[prefix, 0] = mu_x
        psi[prefix, 1] = mu_y
        psi[prefix, 2] = _sign_pm(mu_x * mu_y) * kappa
    mean, sd = _normalize(psi, ctx["P_a"])
    c_mat = _embed_matrix(sd, q_matrix)
    slope = {}
    for prefix in range(16):
        slope[prefix] = diag3(1.0, 1.0, CHI[classes[prefix]]) @ c_mat
    pc_bounds = {}
    for eps in EPS:
        step = float(eps)
        pc_bounds[eps] = {"mu_x": step * float(sd[0]), "mu_y": step * float(sd[1])}
    systems["SYS-PC"] = _finish_system(
        run, ctx, "SYS-PC", ctx["theta"].copy(), slope, set(), mean, sd,
        {
            "C": c_mat,
            "psi": psi,
            "chart": "true",
            "readout": "affine within a fixed sign branch",
            "crossing_bounds": pc_bounds,
            "min_abs_mu_x": float(np.min(np.abs(ctx["theta"][:, 0]))),
            "min_abs_mu_y": float(np.min(np.abs(ctx["theta"][:, 1]))),
        },
    )

    # SYS-FK
    mu = ctx["theta"][:, :2].copy()
    mean, sd = _normalize(mu, ctx["P_a"])
    c_mu = _embed_matrix(sd, q2)
    baseline = np.zeros((16, 3), dtype=np.float64)
    baseline[:, :2] = mu
    slope = {}
    stacked = np.zeros((3, 8), dtype=np.float64)
    stacked[:2, :] = c_mu
    for prefix in range(16):
        slope[prefix] = stacked
    void_rows, voids = _void_report(baseline)
    systems["SYS-FK"] = _finish_system(
        run, ctx, "SYS-FK", baseline, slope, voids, mean, sd,
        {"C_mu": c_mu, "chart": "product", "readout": "affine", "void_rows": void_rows, "C_full": stacked},
    )

    # SYS-NC1 refit, then c2/c3, then the three confound charts.
    # RL-1: rho_NC1 uses the refitted g and the exact-law chart on a=0..15.
    # It is computed before SYS-NC1 voiding and admissibility exist.
    refit = _refit_nc1(run, ctx, committed_g)
    rms = rho_nc1_exact_law(refit["coef"], ctx["theta"][:, 0], ctx["theta"][:, 1], ctx["P_a_exact"])
    ctx["nc1_coef"] = refit["coef"]
    ctx["c2"] = rms["c2"]
    ctx["c3"] = rms["c3"]

    def nc_system(name: str, kappa_of, gradient_of):
        mean_mu, sd_mu = _normalize(mu, ctx["P_a"])
        local_c = _embed_matrix(sd_mu, q2)
        local_base = np.zeros((16, 3), dtype=np.float64)
        local_slope = {}
        for prefix in range(16):
            mu_x = float(mu[prefix, 0])
            mu_y = float(mu[prefix, 1])
            local_base[prefix, 0] = mu_x
            local_base[prefix, 1] = mu_y
            local_base[prefix, 2] = float(kappa_of(prefix, mu_x, mu_y))
            grad = np.asarray(gradient_of(prefix, mu_x, mu_y), dtype=np.float64)
            block = np.zeros((3, 8), dtype=np.float64)
            block[:2, :] = local_c
            block[2, :] = grad @ local_c
            local_slope[prefix] = block
        local_voids_rows, local_voids = _void_report(local_base)
        return _finish_system(
            run, ctx, name, local_base, local_slope, local_voids, mean_mu, sd_mu,
            {
                "C_mu": local_c,
                "chart": name,
                "readout": "nonlinear" if name in ("SYS-NC1", "SYS-NC3") else "affine",
                "void_rows": local_voids_rows,
            },
        )

    systems["SYS-NC1"] = nc_system(
        "SYS-NC1",
        lambda prefix, mu_x, mu_y: g_value(refit["coef"], mu_x, mu_y),
        lambda prefix, mu_x, mu_y: g_gradient(refit["coef"], mu_x, mu_y),
    )
    c2 = float(rms["c2"])
    c3 = float(rms["c3"])
    systems["SYS-NC2"] = nc_system(
        "SYS-NC2",
        lambda prefix, mu_x, mu_y: c2 * mu_x,
        lambda prefix, mu_x, mu_y: (c2, 0.0),
    )
    systems["SYS-NC3"] = nc_system(
        "SYS-NC3",
        lambda prefix, mu_x, mu_y: c3 * (mu_x ** 3),
        lambda prefix, mu_x, mu_y: (3.0 * c3 * (mu_x ** 2), 0.0),
    )

    # SYS-LIM
    mu_a = abs(ctx["charts_exact"][0][0])
    mu_d = abs(ctx["charts_exact"][3][0])
    t_exact = (mu_a + mu_d) / 2
    if t_exact != Fraction(EXACT_T):
        integrity_stop(
            "exact recomputed t does not match the frozen rational",
            recomputed=fraction_text(t_exact),
            frozen=EXACT_T,
        )
    t_float = float(t_exact)
    signs = {}
    psi_lim = np.zeros((16, 3), dtype=np.float64)
    for prefix in range(16):
        mu_x = float(ctx["theta"][prefix, 0])
        mu_y = float(ctx["theta"][prefix, 1])
        kappa = float(ctx["theta"][prefix, 2])
        gap = abs(mu_x) - t_float
        sign = _sign_pm(gap)
        signs[prefix] = sign
        psi_lim[prefix, 0] = mu_x
        psi_lim[prefix, 1] = mu_y
        psi_lim[prefix, 2] = float(sign) * kappa
    mean, sd = _normalize(psi_lim, ctx["P_a"])
    c_lim = _embed_matrix(sd, q_matrix)
    slope = {}
    for prefix in range(16):
        slope[prefix] = diag3(1.0, 1.0, float(signs[prefix])) @ c_lim
    orbit_sign = {}
    for orbit, members in ORBITS.items():
        orbit_sign[orbit] = signs[members[0]]
    lim_bounds = {eps: {"mu_x": float(eps) * float(sd[0])} for eps in EPS}
    margin = float(min(abs(abs(float(ctx["theta"][prefix, 0])) - t_float) for prefix in range(16)))
    systems["SYS-LIM"] = _finish_system(
        run, ctx, "SYS-LIM", ctx["theta"].copy(), slope, set(), mean, sd,
        {
            "C": c_lim,
            "psi": psi_lim,
            "signs": signs,
            "orbit_sign": orbit_sign,
            "t_exact": fraction_text(t_exact),
            "t_float": t_float,
            "chart": "true",
            "readout": "affine within a fixed threshold branch",
            "crossing_bounds": lim_bounds,
            "margin": margin,
            "declared_signs": {"A": 1, "B": -1, "C": -1, "D": -1},
            "sign_matches_declared": orbit_sign == {"A": 1, "B": -1, "C": -1, "D": -1},
        },
    )

    ctx["systems"] = systems
    ctx["classes"] = classes
    public = []
    for name in SYSTEM_ORDER:
        system = systems[name]
        public.append(
            {
                "system": name,
                "admissible": system["admissible"],
                "voided_prefixes": system["voided_prefixes"],
                "normalization": system["normalization"],
                "hashes": system["hashes"],
                "readout": system.get("readout"),
                "chart": system.get("chart"),
            }
        )
    payload = {
        "stage": "S3",
        "representative_mu_positive": representative_positive,
        "systems": public,
        "nc1_g": {
            "coefficients": refit["coefficients"],
            "committed_coefficients": refit["committed_coefficients"],
            "max_abs_diff": refit["max_abs_diff"],
            "tolerance": refit["tolerance"],
            "exact_reduction_to_cross_term": refit["exact_reduction_to_cross_term"],
            "exact_reduction_note": refit["exact_reduction_note"],
            "rank_report": {
                "system": "SYS-NC1",
                "fit_type": None,
                "fold": None,
                "class": None,
                "map": "nc1_g",
                "n_rows": refit["n_rows"],
                "n_cols": refit["n_cols"],
                "sigma": refit["sigma"],
                "sigma_1": refit["sigma_1"],
                "ratios": refit["ratios"],
                "rank_category": refit["rank_category"],
                "n_inverted": refit["n_inverted"],
                "b3_status": None,
            },
        },
        "rms": {
            key: rms[key]
            for key in (
                "rho_NC1",
                "M4",
                "P_sum_float",
                "c2",
                "c3",
                "summation_order",
                "n_prefixes",
                "prefix_domain",
                "independent_of_sys_nc1_voids",
                "independent_of_sys_nc1_admissibility",
                "e39_7_skip_applied",
                "unit",
            )
        },
        "t_exact": systems["SYS-LIM"]["t_exact"],
        "crossing_bounds": {
            "SYS-PC": systems["SYS-PC"]["crossing_bounds"],
            "SYS-LIM": systems["SYS-LIM"]["crossing_bounds"],
        },
        "memory": run.memory_observation(),
    }
    run.write_json("stage_S3_construction.json", payload)
    run.checkpoint("S3")
    run.log("stage S3 written")
    return systems
