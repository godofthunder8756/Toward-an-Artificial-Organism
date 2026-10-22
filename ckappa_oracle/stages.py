"""Oracle stages O1, O2, O6, O7, O3, O4, O5.

Propagation order inside O6 and O7, frozen here and in the manifest:
folds in listed order, evaluation prefixes ascending, continuation u = 0..15,
direction rows in draw order, signs +1 then -1, eps_syn in listed order,
and for each edit the kinds actual, Pred_full, Pred_mu. The true or O7
baseline Phi for that (prefix, continuation) is the call immediately before
those three kinds, on first use.
"""

from __future__ import annotations

import hashlib
import math
import time
from fractions import Fraction

import numpy as np

from ckappa_oracle.geometry import (
    FOLD_SPEC,
    GROUPS,
    ORBITS,
    SECTION5_GROUPS,
    folds,
    g_gradient,
    g_value,
    monomials,
    squared_error,
    weighted_mean_and_sd,
)
from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_oracle.linalg_fit import fit_from_svd, singular_values
from ckappa_oracle.outcomes import classify_group
from ckappa_oracle.pinned import DECLARED_N_O1, FROZEN_RUNTIME, fnum
from ckappa_oracle import world

GUARD = fnum("guard")
O2_TOL = fnum("o2_tolerance")
O6_TOL = fnum("o6_tolerance")
FD_STEP = fnum("fd_step")
BAND_LO = fnum("rank_resolved_zero_below")
BAND_HI = fnum("rank_resolved_above")
SIGMA3_STOP = fnum("o7_sigma3_stop_above")
EPS_SYN = tuple(FROZEN_RUNTIME["eps_syn"])
O4_SIZES = tuple(FROZEN_RUNTIME["o4_sizes"])
REFERENCE_EPS = FROZEN_RUNTIME["reference_eps_syn"]
EDITS_PER_FOLD = 8 * 16 * 16 * 2


def _fail(reason: str, **detail):
    payload = {"reason": reason}
    payload.update(detail)
    raise PackageStop("PIPELINE INVALID", 2, payload)


def _matrix_sha(matrix: np.ndarray) -> str:
    raw = np.ascontiguousarray(matrix, dtype="<f8")
    return hashlib.sha256(raw.tobytes()).hexdigest()


def _lists(matrix: np.ndarray):
    return np.asarray(matrix, dtype=np.float64).tolist()


def _as_bmu(solution):
    """Pad a 2-row chart solution with a zero kappa row."""
    if solution is None:
        return None
    full = np.zeros((3, solution.shape[1]), dtype=np.float64)
    full[:2, :] = solution
    return full


def _accept_exact(got, expected, truncation: str) -> bool:
    if got == expected:
        return True
    return world.decimal_truncation_50(got) == truncation


def _valid(belief: np.ndarray) -> bool:
    return bool(np.all(np.asarray(belief, dtype=np.float64) >= GUARD))


def _key_public(key) -> list:
    public = []
    for part in key:
        if isinstance(part, (str, int, float, bool)) or part is None:
            public.append(part)
        else:
            public.append(str(part))
    return public


def _propagate_three(run, thetas, continuation: int, bucket: str, key_prefix, scoreable: bool, counts: dict):
    """Propagate every edit. Guard failures are counted and stored as null. Scoreable failures stop."""
    outputs = []
    for kind, theta in thetas:
        key = key_prefix + (kind,)
        try:
            forecast, _belief = run.phi(theta, continuation, bucket, key)
        except ValueError as exc:
            if scoreable:
                _fail(
                    "scoreable edit",
                    bucket=bucket,
                    failure="ValueError",
                    error=str(exc),
                    edit=_key_public(key),
                )
            counts["value_error"] += 1
            outputs.append(None)
            continue
        if not np.all(np.isfinite(forecast)):
            if scoreable:
                _fail("scoreable edit", bucket=bucket, failure="non-finite", edit=_key_public(key))
            counts["non_finite"] += 1
            outputs.append(None)
            continue
        outputs.append(forecast)
    return outputs


def _not_propagated_row(fold: str, eps: str) -> dict:
    return {
        "fold": fold,
        "eps_syn": eps,
        "not_propagated": "not propagated",
        "n_scoreable": None,
        "n_total": None,
        "mass_coverage": None,
    }


def _coverage_report(tables, scored, unresolved_folds) -> dict:
    coverage = {}
    for eps in EPS_SYN:
        rows = _coverage_rows(tables, eps, scored) if scored else []
        rows.extend(_not_propagated_row(fold, eps) for fold in unresolved_folds)
        coverage[eps] = rows
    return coverage


def stage_o1(run, stored: dict) -> dict:
    run.check_deadline("O1")
    started = time.perf_counter()
    matrix = world.fraction_transition()
    beliefs = []
    prefix_probability = []
    for prefix in range(16):
        belief, probability = world.filter_prefix(prefix, 4, matrix)
        run.bump_exact(1)
        beliefs.append(belief)
        prefix_probability.append(probability)
    forecasts = {}
    history_probability = {}
    terminals = {}
    mismatches = []
    for prefix in range(16):
        for continuation in range(16):
            terminal, predictive = world.propagate_exact(beliefs[prefix], continuation, matrix)
            run.bump_exact(1)
            history = prefix + 16 * continuation
            probability = prefix_probability[prefix] * predictive
            qx, qy, qxor = world.forecasts_from_belief(terminal)
            forecasts[history] = (qx, qy, qxor)
            history_probability[history] = probability
            terminals[history] = terminal
            row = stored[history]
            checks = (
                ("q_X", qx, row["marginal_x"], row["marginal_x_truncation_50"]),
                ("q_Y", qy, row["marginal_y"], row["marginal_y_truncation_50"]),
                ("q_XOR", qxor, row["xor_joint"], row["xor_joint_truncation_50"]),
                ("P", probability, row["probability"], row["probability_truncation_50"]),
            )
            for name, got, expected, truncation in checks:
                if not _accept_exact(got, expected, truncation):
                    mismatches.append(
                        {
                            "history": history,
                            "quantity": name,
                            "got": world.fraction_text(got),
                            "expected": world.fraction_text(expected),
                        }
                    )
    failures = []
    if mismatches:
        failures.append({"check": "terminal forecasts or P(h)", "mismatch_count": len(mismatches)})
    if sum(history_probability.values(), start=Fraction(0)) != 1:
        failures.append({"check": "history probabilities sum to 1"})
    for prefix in range(16):
        mass = sum((history_probability[prefix + 16 * continuation] for continuation in range(16)), start=Fraction(0))
        if mass != prefix_probability[prefix]:
            failures.append({"check": "prefix probability", "prefix": prefix})
            break
    for belief in list(beliefs) + list(terminals.values()):
        chart, marginals = world.chart_from_belief(belief)
        rebuilt = world.belief_from_chart_exact(*marginals)
        if rebuilt != list(belief):
            failures.append({"check": "chart round-trip"})
            break
        mx, my, c = world.marginals_covariance(rebuilt)
        if (mx, my, c) != marginals:
            failures.append({"check": "chart marginal recovery"})
            break
        del chart
    for prefix, belief in enumerate(beliefs):
        for mask, flip_mu_x, flip_mu_y in ((5, True, False), (10, False, True)):
            other = beliefs[prefix ^ mask]
            left, _ = world.chart_from_belief(belief)
            right, _ = world.chart_from_belief(other)
            expected = (
                -left[0] if flip_mu_x else left[0],
                -left[1] if flip_mu_y else left[1],
                -left[2],
            )
            if right != expected or prefix_probability[prefix] != prefix_probability[prefix ^ mask]:
                failures.append({"check": "stage-4 flip", "prefix": prefix, "mask": mask})
                break
    for history, belief in terminals.items():
        for mask, flip_mu_x, flip_mu_y in ((85, True, False), (170, False, True)):
            other = terminals[history ^ mask]
            left, _ = world.chart_from_belief(belief)
            right, _ = world.chart_from_belief(other)
            expected = (
                -left[0] if flip_mu_x else left[0],
                -left[1] if flip_mu_y else left[1],
                -left[2],
            )
            if right != expected or history_probability[history] != history_probability[history ^ mask]:
                failures.append({"check": "terminal flip", "history": history, "mask": mask})
                break
        else:
            continue
        break
    orbit_ok = True
    covered = set()
    for name, members in ORBITS.items():
        member_set = set(members)
        covered |= member_set
        if len(member_set) != 4:
            orbit_ok = False
        for prefix in member_set:
            images = {prefix ^ mask for mask in (0, 5, 10, 15)}
            if images != member_set:
                orbit_ok = False
    if covered != set(range(16)) or not orbit_ok:
        failures.append({"check": "orbits or free flip action"})
    test_count = sum(1 for prefix in range(16) for continuation in range(16) if (prefix + continuation) % 4 == 0)
    train_count = 256 - test_count
    if test_count != 64 or train_count != 192:
        failures.append({"check": "TEST/TRAIN counts", "test": test_count, "train": train_count})
    eval_counts = {prefix: 0 for prefix in range(16)}
    for _name, _fit, evaluation in folds():
        for prefix in evaluation:
            eval_counts[prefix] += 1
    if any(value != 3 for value in eval_counts.values()):
        failures.append({"check": "each prefix is an evaluation prefix in 3 folds"})
    n_exact = run.exact_count
    if n_exact != DECLARED_N_O1:
        failures.append({"check": "exact propagation count", "n_O1": n_exact, "declared": DECLARED_N_O1})
    run.t_o1 = time.perf_counter() - started
    run.n_o1 = n_exact
    split_table = []
    for prefix in range(16):
        for continuation in range(16):
            val_excluded = continuation == ((2 - prefix) % 16)
            split_table.append(
                {
                    "a": prefix,
                    "u": continuation,
                    "h": prefix + 16 * continuation,
                    "test": (prefix + continuation) % 4 == 0,
                    "val": (prefix + continuation) % 4 == 2 and not val_excluded,
                    "fit_folds": [name for name, fit, _evaluation in folds() if prefix in fit],
                    "eval_folds": [name for name, _fit, evaluation in folds() if prefix in evaluation],
                }
            )
    theta = np.zeros((16, 3), dtype=np.float64)
    theta_exact = []
    for prefix, belief in enumerate(beliefs):
        chart, _marginals = world.chart_from_belief(belief)
        theta_exact.append([world.fraction_text(value) for value in chart])
        theta[prefix, :] = [float(value) for value in chart]
    p_h = {}
    p_a = np.zeros(16, dtype=np.float64)
    for prefix in range(16):
        for continuation in range(16):
            probability = float(history_probability[prefix + 16 * continuation])
            p_h[(prefix, continuation)] = probability
            p_a[prefix] += probability
    payload = {
        "status": "FAIL" if failures else "PASS",
        "n_O1": n_exact,
        "T_O1_s": run.t_o1,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:64],
        "failures": failures,
        "test_count": test_count,
        "train_count": train_count,
        "orbits": {name: list(members) for name, members in ORBITS.items()},
        "fold_spec": [
            {"fold": name, "fit_orbits": list(fit), "eval_orbits": list(evaluation)}
            for name, fit, evaluation in FOLD_SPEC
        ],
        "stage4_chart_exact": theta_exact,
        "split_table": split_table,
        "val_readout_rejection": "UNVERIFIED",
        "continuation_strings_shared": True,
    }
    run.write_stage("O1", payload)
    if failures:
        _fail("O1 fixture", failures=failures, mismatch_count=len(mismatches))
    return {
        "theta": theta,
        "P_h": p_h,
        "P_a": p_a,
        "forecasts_exact": forecasts,
        "L": {},
    }


def _embed(ctx: dict, draws: dict) -> None:
    mean, sd = weighted_mean_and_sd(ctx["theta"], ctx["P_a"])
    if np.any(sd == 0.0) or not np.all(np.isfinite(sd)):
        integrity_stop("P-weighted chart standard deviation is 0")
    ctx["mean"] = mean
    ctx["sd"] = sd
    ctx["B_true"] = np.diag(sd) @ draws["Q"].T


def stage_o2(run, ctx: dict) -> None:
    run.check_deadline("O2")
    max_abs = 0.0
    worst = None
    n_entries = 0
    for prefix in range(16):
        theta = ctx["theta"][prefix]
        for continuation in range(16):
            try:
                closed = world.closed_form_L(theta, continuation, run.transition)
            except ValueError as exc:
                _fail("closed-form derivative", prefix=prefix, continuation=continuation, error=str(exc))
            finite = np.empty((3, 3), dtype=np.float64)
            for coordinate in range(3):
                plus = theta.copy()
                minus = theta.copy()
                plus[coordinate] += FD_STEP
                minus[coordinate] -= FD_STEP
                try:
                    q_plus, _belief = run.phi(plus, continuation, "O2", ("O2", prefix, continuation, coordinate, 1))
                    q_minus, _belief = run.phi(minus, continuation, "O2", ("O2", prefix, continuation, coordinate, -1))
                except ValueError as exc:
                    _fail("finite-difference derivative", prefix=prefix, continuation=continuation, error=str(exc))
                finite[:, coordinate] = (q_plus - q_minus) / (2.0 * FD_STEP)
            difference = float(np.max(np.abs(closed - finite)))
            n_entries += 9
            if difference >= max_abs:
                max_abs = difference
                worst = {"prefix": prefix, "continuation": continuation, "max_abs": difference}
            ctx["L"][(prefix, continuation)] = closed
    status = "PASS" if max_abs <= O2_TOL else "FAIL"
    run.write_stage(
        "O2",
        {
            "status": status,
            "max_abs_difference": max_abs,
            "tolerance": O2_TOL,
            "fd_step": FD_STEP,
            "entries": n_entries,
            "float_propagations": run.bucket["O2"],
            "worst": worst,
        },
    )
    if status == "FAIL":
        _fail("O2 fixture", max_abs_difference=max_abs, tolerance=O2_TOL)
    if run.bucket["O2"] != 16 * 16 * 3 * 2:
        integrity_stop("O2 propagation count", count=run.bucket["O2"])


def _fit_blocks(prefixes, columns: int, L_of, J_of, p_h):
    design_rows = []
    target_rows = []
    for prefix in prefixes:
        for continuation in range(16):
            local_l = L_of(prefix, continuation)
            local_j = J_of(prefix, continuation)
            scale = math.sqrt(p_h[(prefix, continuation)])
            block = local_l if columns == 3 else local_l[:, :2]
            design_rows.append(scale * block)
            target_rows.append(scale * local_j)
    if not design_rows:
        return None, None
    return np.vstack(design_rows), np.vstack(target_rows)


def _loss_tables():
    return {"loss": {}, "coverage": {}}


def _add_coverage(tables, fold: str, eps: str, weight: float, scoreable: bool) -> None:
    row = tables["coverage"].setdefault(
        (fold, eps),
        {"n_scoreable": 0, "n_total": 0, "mass_scoreable": 0.0, "mass_total": 0.0},
    )
    row["n_total"] += 1
    row["mass_total"] += weight
    if scoreable:
        row["n_scoreable"] += 1
        row["mass_scoreable"] += weight


def _add_loss(tables, fold, eps, group, weight, se_mu, se_full, se_actual) -> None:
    for mode, factor in (("weighted", weight), ("unweighted", 1.0)):
        row = tables["loss"].setdefault(
            (mode, fold, eps, group),
            {"H": 0.0, "L": 0.0, "S": 0.0, "den": 0.0, "n": 0},
        )
        row["H"] += factor * se_mu
        row["L"] += factor * se_full
        row["S"] += factor * se_actual
        row["den"] += factor
        row["n"] += 1


def _pool(tables, mode, eps, group, fold_names):
    total_h = total_l = total_s = denominator = 0.0
    count = 0
    for fold in fold_names:
        row = tables["loss"].get((mode, fold, eps, group))
        if row is None:
            continue
        total_h += row["H"]
        total_l += row["L"]
        total_s += row["S"]
        denominator += row["den"]
        count += row["n"]
    if denominator == 0.0:
        return {
            "H": None,
            "L_full": None,
            "S": None,
            "R": "UNDEFINED",
            "measured_gain": None,
            "denominator": 0.0,
            "n": 0,
        }
    h_value = total_h / denominator
    l_value = total_l / denominator
    s_value = total_s / denominator
    return {
        "H": h_value,
        "L_full": l_value,
        "S": s_value,
        "R": "UNDEFINED" if s_value == 0.0 else h_value / s_value,
        "measured_gain": h_value - l_value,
        "denominator": denominator,
        "n": count,
    }


def _coverage_rows(tables, eps: str, fold_names):
    rows = []
    for fold in fold_names:
        row = tables["coverage"][(fold, eps)]
        if row["mass_total"] == 0.0:
            integrity_stop("coverage mass total is 0", fold=fold, eps_syn=eps)
        rows.append(
            {
                "fold": fold,
                "eps_syn": eps,
                "n_scoreable": row["n_scoreable"],
                "n_total": row["n_total"],
                "mass_coverage": row["mass_scoreable"] / row["mass_total"],
                "mass_scoreable": row["mass_scoreable"],
                "mass_total": row["mass_total"],
                "losses_conditional_on_scoreable_subset": True,
            }
        )
    return rows


def _section5(scored_folds, unresolved: bool, tables):
    coverage = _coverage_rows(tables, REFERENCE_EPS, scored_folds) if scored_folds else []
    out = {}
    for group in SECTION5_GROUPS:
        pooled = None if unresolved else _pool(tables, "weighted", REFERENCE_EPS, group, scored_folds)
        out[group] = classify_group(group, coverage, unresolved, pooled)
    return out


def stage_o6(run, ctx: dict, draws: dict) -> dict:
    run.check_deadline("O6")
    run.on_sample = run.project
    b_true = ctx["B_true"]
    fold_rows = []
    identity_failure = None
    for name, fit_prefixes, _evaluation in folds():
        def L_of(prefix, continuation, _store=ctx["L"]):
            return _store[(prefix, continuation)]

        def J_of(prefix, continuation, _b=b_true):
            return L_of(prefix, continuation) @ _b

        design_b, target_b = _fit_blocks(fit_prefixes, 3, L_of, J_of, ctx["P_h"])
        design_mu, target_mu = _fit_blocks(fit_prefixes, 2, L_of, J_of, ctx["P_h"])
        solution_b, report_b = fit_from_svd(design_b, target_b)
        solution_mu, report_mu = fit_from_svd(design_mu, target_mu)
        solution_mu = _as_bmu(solution_mu)
        scored = bool(report_b["scored"] and report_mu["scored"])
        b_error = None
        if scored:
            b_error = float(np.max(np.abs(solution_b - b_true)))
            if b_error > O6_TOL and identity_failure is None:
                identity_failure = {"fold": name, "B_max_abs_error": b_error}
        fold_rows.append(
            {
                "fold": name,
                "fit_prefixes": list(fit_prefixes),
                "scored": scored,
                "B": None if solution_b is None else solution_b,
                "B_mu": None if solution_mu is None else solution_mu,
                "B_report": report_b,
                "B_mu_report": report_mu,
                "B_max_abs_error": b_error,
                "B_sha256": None if solution_b is None else _matrix_sha(solution_b),
                "B_mu_sha256": None if solution_mu is None else _matrix_sha(solution_mu),
            }
        )
    freeze = []
    for row in fold_rows:
        freeze.append(
            {
                "fold": row["fold"],
                "scored": row["scored"],
                "B_sha256": row["B_sha256"],
                "B_mu_sha256": row["B_mu_sha256"],
                "B": None if row["B"] is None else _lists(row["B"]),
                "B_mu": None if row["B_mu"] is None else _lists(row["B_mu"]),
                "B_rank": row["B_report"],
                "B_mu_rank": row["B_mu_report"],
                "B_max_abs_error": row["B_max_abs_error"],
            }
        )
    run.write_json("outputs/fit_freeze_O6.json", {"fits": freeze, "identity_failure": identity_failure})
    if identity_failure is not None:
        run.write_stage("O6", {"status": "FAIL", "identity_failure": identity_failure, "fits": freeze})
        _fail("O6 B identity", **identity_failure)

    tables = _loss_tables()
    worst = {"max_abs": 0.0, "edit": None}
    guard_failures = {"value_error": 0, "non_finite": 0}
    directions = draws["O6_directions"]
    try:
        for row, (_name, _fit, evaluation) in zip(fold_rows, folds()):
            if not row["scored"]:
                continue
            for prefix in evaluation:
                theta = ctx["theta"][prefix]
                for continuation in range(16):
                    q_base, _base_belief = run.phi_cached(
                        ("true", prefix, continuation),
                        theta,
                        continuation,
                        "O6",
                    )
                    weight = ctx["P_h"][(prefix, continuation)]
                    for direction_index, direction in enumerate(directions):
                        for sign in (1.0, -1.0):
                            for eps in EPS_SYN:
                                delta = float(eps) * sign * direction
                                theta_actual = theta + b_true @ delta
                                theta_full = theta + row["B"] @ delta
                                theta_mu = theta + row["B_mu"] @ delta
                                belief_actual = world.inverse_chart_float(theta_actual)
                                belief_full = world.inverse_chart_float(theta_full)
                                belief_mu = world.inverse_chart_float(theta_mu)
                                scoreable = _valid(belief_actual) and _valid(belief_full) and _valid(belief_mu)
                                q_actual, q_full, q_mu = _propagate_three(
                                    run,
                                    (
                                        ("actual", theta_actual),
                                        ("Pred_full", theta_full),
                                        ("Pred_mu", theta_mu),
                                    ),
                                    continuation,
                                    "O6",
                                    ("O6", row["fold"], prefix, continuation, direction_index, sign, eps),
                                    scoreable,
                                    guard_failures,
                                )
                                _add_coverage(tables, row["fold"], eps, weight, scoreable)
                                if not scoreable:
                                    continue
                                actual = q_actual - q_base
                                pred_full = q_full - q_base
                                pred_mu = q_mu - q_base
                                error = float(np.max(np.abs(pred_full - actual)))
                                if error > worst["max_abs"]:
                                    worst = {
                                        "max_abs": error,
                                        "edit": {
                                            "fold": row["fold"],
                                            "prefix": prefix,
                                            "continuation": continuation,
                                            "direction": direction_index,
                                            "sign": sign,
                                            "eps_syn": eps,
                                        },
                                    }
                                if error > O6_TOL:
                                    run.write_stage(
                                        "O6",
                                        {
                                            "status": "FAIL",
                                            "Pred_full_max_abs_error": error,
                                            "tolerance": O6_TOL,
                                            "worst": worst,
                                        },
                                    )
                                    _fail("O6 Pred_full identity", max_abs_error=error, edit=worst["edit"])
                                for group in GROUPS:
                                    _add_loss(
                                        tables,
                                        row["fold"],
                                        eps,
                                        group,
                                        weight,
                                        squared_error(actual - pred_mu, group),
                                        squared_error(actual - pred_full, group),
                                        squared_error(actual, group),
                                    )
    except PackageStop:
        raise
    scored = [row["fold"] for row in fold_rows if row["scored"]]
    for fold in scored:
        for eps in EPS_SYN:
            if tables["coverage"][(fold, eps)]["n_total"] != EDITS_PER_FOLD:
                integrity_stop(
                    "O6 edit count",
                    fold=fold,
                    eps_syn=eps,
                    n_total=tables["coverage"][(fold, eps)]["n_total"],
                )
    unresolved_folds = [row["fold"] for row in fold_rows if not row["scored"]]
    unresolved = bool(unresolved_folds)
    coverage = _coverage_report(tables, scored, unresolved_folds)
    pooled = {}
    per_fold = {}
    if not unresolved:
        for eps in EPS_SYN:
            pooled[eps] = {
                group: {
                    "weighted": _pool(tables, "weighted", eps, group, scored),
                    "unweighted": _pool(tables, "unweighted", eps, group, scored),
                }
                for group in GROUPS
            }
            per_fold[eps] = {
                group: {fold: _pool(tables, "weighted", eps, group, [fold]) for fold in scored}
                for group in GROUPS
            }
    section5 = _section5(scored, unresolved, tables)
    public_fits = []
    for row in fold_rows:
        public_fits.append(
            {
                "fold": row["fold"],
                "scored": row["scored"],
                "fit_prefix_count": len(row["fit_prefixes"]),
                "B_sha256": row["B_sha256"],
                "B_mu_sha256": row["B_mu_sha256"],
                "B_max_abs_error": row["B_max_abs_error"],
                "B_rank": row["B_report"],
                "B_mu_rank": row["B_mu_report"],
            }
        )
    payload = {
        "status": "PASS",
        "fits": public_fits,
        "Pred_full_max_abs_error": worst["max_abs"],
        "Pred_full_worst_edit": worst["edit"],
        "Pred_full_tolerance": O6_TOL,
        "coverage": coverage,
        "pooled": pooled,
        "pooled_section5_statistic": "not_formed" if unresolved else "formed",
        "per_fold_weighted": per_fold,
        "section5_from_o6": section5,
        "losses_conditional_on_scoreable_subset": True,
        "guard_failing_phi": guard_failures,
    }
    run.write_stage("O6", payload)
    return section5


def _sigma_report(values: np.ndarray | None) -> dict:
    if values is None or values.size == 0:
        return {
            "sigma_1": None,
            "ratios": None,
            "ratios_formed": False,
            "third_ratio": None,
            "stop": False,
            "unresolved": False,
            "note": "no stacked rows",
        }
    if float(values[0]) == 0.0:
        return {
            "sigma": [float(value) for value in values],
            "sigma_1": 0.0,
            "ratios": None,
            "ratios_formed": False,
            "third_ratio": None,
            "stop": False,
            "unresolved": False,
            "note": "sigma_1 is 0; ratios not formed; resolved rank 0",
        }
    ratios = values / float(values[0])
    unresolved = bool(np.any((ratios >= BAND_LO) & (ratios <= BAND_HI)))
    third = float(ratios[2]) if ratios.size >= 3 else None
    stop = third is not None and third > SIGMA3_STOP
    return {
        "sigma": [float(value) for value in values],
        "sigma_1": float(values[0]),
        "ratios": [float(value) for value in ratios],
        "ratios_formed": True,
        "third_ratio": third,
        "stop": stop,
        "unresolved": unresolved,
        "note": "resolved third direction" if stop else ("unresolved" if unresolved else "resolved lower or full rank within two"),
    }


def _o7_chart(theta_row: np.ndarray, coef: np.ndarray) -> np.ndarray:
    mu_x = float(theta_row[0])
    mu_y = float(theta_row[1])
    return np.array([mu_x, mu_y, g_value(coef, mu_x, mu_y)], dtype=np.float64)


def stage_o7(run, ctx: dict, draws: dict) -> None:
    run.check_deadline("O7")
    design_rows = []
    target = []
    for prefix in range(16):
        mu_x = float(ctx["theta"][prefix, 0])
        mu_y = float(ctx["theta"][prefix, 1])
        kappa = float(ctx["theta"][prefix, 2])
        scale = math.sqrt(float(ctx["P_a"][prefix]))
        design_rows.append(scale * monomials(mu_x, mu_y))
        target.append(scale * kappa)
    coef, g_report = fit_from_svd(np.vstack(design_rows), np.asarray(target, dtype=np.float64))
    if not g_report["scored"]:
        run.write_stage(
            "O7",
            {
                "status": "G RANK UNRESOLVED",
                "label": "g rank UNRESOLVED",
                "g_rank": g_report,
                "derivatives_evaluated": False,
                "predictions_evaluated": False,
                "sigma_report": "not_formed",
            },
        )
        return
    voided = []
    for prefix in range(16):
        chart = _o7_chart(ctx["theta"][prefix], coef)
        belief = world.inverse_chart_float(chart)
        if not _valid(belief):
            voided.append(
                {
                    "prefix": prefix,
                    "label": "RESTRICTED COMPARATOR NOT ADMISSIBLE",
                    "min_p": float(np.min(belief)),
                }
            )
    void_ids = {item["prefix"] for item in voided}
    admissible = len(voided) < int(FROZEN_RUNTIME["o7_void_stop_count"])
    kappa_error = []
    for prefix in range(16):
        mu_x = float(ctx["theta"][prefix, 0])
        mu_y = float(ctx["theta"][prefix, 1])
        kappa = float(ctx["theta"][prefix, 2])
        kappa_hat = g_value(coef, mu_x, mu_y)
        kappa_error.append(
            {
                "prefix": prefix,
                "kappa_hat_minus_kappa": kappa_hat - kappa,
                "voided": prefix in void_ids,
            }
        )
    other = [abs(float(coef[index])) for index in (0, 1, 2, 3, 5)]
    base = {
        "g_coefficients": [float(value) for value in coef],
        "g_rank": g_report,
        "exact_reduction_to_cross_term": all(value == 0.0 for value in other),
        "voided_prefixes": voided,
        "voided_count": len(voided),
        "kappa_error": kappa_error,
        "admissible": admissible,
    }
    mean2 = ctx["mean"][:2]
    sd2 = ctx["sd"][:2]
    q2 = draws["Q2"]
    dmu = np.diag(sd2) @ q2.T

    def dtheta_dz(prefix: int) -> np.ndarray:
        gradient = g_gradient(coef, float(ctx["theta"][prefix, 0]), float(ctx["theta"][prefix, 1]))
        jacobian = np.zeros((3, 8), dtype=np.float64)
        jacobian[:2, :] = dmu
        jacobian[2, :] = gradient @ dmu
        return jacobian

    sigma_rows = []
    stop = False
    for name, fit_prefixes, _evaluation in folds():
        blocks = []
        used = []
        for prefix in fit_prefixes:
            if prefix in void_ids:
                continue
            used.append(prefix)
            chart = _o7_chart(ctx["theta"][prefix], coef)
            factor = dtheta_dz(prefix)
            for continuation in range(16):
                local_l = world.closed_form_L(chart, continuation, run.transition)
                blocks.append(local_l @ factor)
        report = _sigma_report(singular_values(np.vstack(blocks)) if blocks else None)
        report["fold"] = name
        report["non_voided_fit_prefixes"] = used
        sigma_rows.append(report)
        if report["stop"]:
            stop = True
    if stop:
        run.write_stage(
            "O7",
            {
                **base,
                "status": "FAIL",
                "sigma": sigma_rows,
                "integrity_diagnosis": (
                    "A resolved third singular direction of the O7 stacked Jacobian "
                    "contradicts the two-coordinate construction. STOP, PIPELINE INVALID. No rerun."
                ),
            },
        )
        _fail("O7 resolved third direction", folds=[row["fold"] for row in sigma_rows if row["stop"]])
    if not admissible:
        run.write_stage(
            "O7",
            {
                **base,
                "status": "RESTRICTED COMPARATOR NOT ADMISSIBLE",
                "label": "RESTRICTED COMPARATOR NOT ADMISSIBLE",
                "sigma": sigma_rows,
                "derivatives_evaluated": False,
                "predictions_evaluated": False,
            },
        )
        return

    # Admissible. Fit on non-voided fit prefixes and score non-voided evaluation prefixes.
    fold_rows = []
    for name, fit_prefixes, evaluation in folds():
        kept_fit = tuple(prefix for prefix in fit_prefixes if prefix not in void_ids)
        kept_eval = tuple(prefix for prefix in evaluation if prefix not in void_ids)

        def L_of(prefix, continuation, _coef=coef):
            return world.closed_form_L(_o7_chart(ctx["theta"][prefix], _coef), continuation, run.transition)

        def J_of(prefix, continuation):
            return L_of(prefix, continuation) @ dtheta_dz(prefix)

        design_b, target_b = _fit_blocks(kept_fit, 3, L_of, J_of, ctx["P_h"])
        design_mu, target_mu = _fit_blocks(kept_fit, 2, L_of, J_of, ctx["P_h"])
        if design_b is None or design_mu is None:
            run.write_stage(
                "O7",
                {
                    **base,
                    "status": "UNRESOLVED",
                    "label": "UNRESOLVED",
                    "empty_reduced_design": name,
                    "sigma": sigma_rows,
                    "derivatives_evaluated": False,
                    "predictions_evaluated": False,
                },
            )
            assert design_b is not None and design_mu is not None, (
                "empty O7 design is not expected to be reachable"
            )
            return
        solution_b, report_b = fit_from_svd(design_b, target_b)
        solution_mu, report_mu = fit_from_svd(design_mu, target_mu)
        solution_mu = _as_bmu(solution_mu)
        fold_rows.append(
            {
                "fold": name,
                "fit_prefixes": list(kept_fit),
                "eval_prefixes": list(kept_eval),
                "scored": bool(report_b["scored"] and report_mu["scored"]),
                "B": solution_b,
                "B_mu": solution_mu,
                "B_report": report_b,
                "B_mu_report": report_mu,
                "B_sha256": None if solution_b is None else _matrix_sha(solution_b),
                "B_mu_sha256": None if solution_mu is None else _matrix_sha(solution_mu),
            }
        )
    run.write_json(
        "outputs/fit_freeze_O7.json",
        {
            "fits": [
                {
                    "fold": row["fold"],
                    "scored": row["scored"],
                    "fit_prefix_count": len(row["fit_prefixes"]),
                    "eval_prefix_count": len(row["eval_prefixes"]),
                    "B_sha256": row["B_sha256"],
                    "B_mu_sha256": row["B_mu_sha256"],
                    "B_rank": row["B_report"],
                    "B_mu_rank": row["B_mu_report"],
                }
                for row in fold_rows
            ]
        },
    )
    disagreement = {group: {"numerator": 0.0, "denominator": 0.0} for group in GROUPS}
    for prefix in range(16):
        if prefix in void_ids:
            continue
        chart = _o7_chart(ctx["theta"][prefix], coef)
        for continuation in range(16):
            q_o7, _belief = run.phi_cached(("o7", prefix, continuation), chart, continuation, "O7_baseline")
            exact = ctx["forecasts_exact"][prefix + 16 * continuation]
            q_true = np.array([float(exact[0]), float(exact[1]), float(exact[2])], dtype=np.float64)
            weight = ctx["P_h"][(prefix, continuation)]
            residual = q_o7 - q_true
            for group in GROUPS:
                disagreement[group]["numerator"] += weight * squared_error(residual, group)
                disagreement[group]["denominator"] += weight
    disagreement_public = {}
    for group, row in disagreement.items():
        if row["denominator"] == 0.0:
            disagreement_public[group] = {"weighted_mean_squared_error": None, "denominator": 0.0}
        else:
            disagreement_public[group] = {
                "weighted_mean_squared_error": row["numerator"] / row["denominator"],
                "denominator": row["denominator"],
            }
    tables = _loss_tables()
    guard_failures = {"value_error": 0, "non_finite": 0}
    directions = draws["O6_directions"]
    for row in fold_rows:
        if not row["scored"]:
            continue
        for prefix in row["eval_prefixes"]:
            chart = _o7_chart(ctx["theta"][prefix], coef)
            mu = ctx["theta"][prefix, :2]
            z_prefix = q2 @ ((mu - mean2) / sd2)
            for continuation in range(16):
                q_base, _belief = run.phi_cached(("o7", prefix, continuation), chart, continuation, "O7_baseline")
                weight = ctx["P_h"][(prefix, continuation)]
                for direction_index, direction in enumerate(directions):
                    for sign in (1.0, -1.0):
                        for eps in EPS_SYN:
                            delta = float(eps) * sign * direction
                            z_new = z_prefix + delta
                            mu_new = mean2 + sd2 * (q2.T @ z_new)
                            theta_actual = np.array(
                                [float(mu_new[0]), float(mu_new[1]), g_value(coef, float(mu_new[0]), float(mu_new[1]))],
                                dtype=np.float64,
                            )
                            theta_full = chart + row["B"] @ delta
                            theta_mu = chart + row["B_mu"] @ delta
                            scoreable = (
                                _valid(world.inverse_chart_float(theta_actual))
                                and _valid(world.inverse_chart_float(theta_full))
                                and _valid(world.inverse_chart_float(theta_mu))
                            )
                            q_actual, q_full, q_mu = _propagate_three(
                                run,
                                (
                                    ("actual", theta_actual),
                                    ("Pred_full", theta_full),
                                    ("Pred_mu", theta_mu),
                                ),
                                continuation,
                                "O7",
                                ("O7", row["fold"], prefix, continuation, direction_index, sign, eps),
                                scoreable,
                                guard_failures,
                            )
                            _add_coverage(tables, row["fold"], eps, weight, scoreable)
                            if not scoreable:
                                continue
                            actual = q_actual - q_base
                            pred_full = q_full - q_base
                            pred_mu = q_mu - q_base
                            for group in GROUPS:
                                _add_loss(
                                    tables,
                                    row["fold"],
                                    eps,
                                    group,
                                    weight,
                                    squared_error(actual - pred_mu, group),
                                    squared_error(actual - pred_full, group),
                                    squared_error(actual, group),
                                )
    scored = [row["fold"] for row in fold_rows if row["scored"]]
    unresolved_folds = [row["fold"] for row in fold_rows if not row["scored"]]
    pooled = {}
    if scored:
        for eps in EPS_SYN:
            pooled[eps] = {
                group: _pool(tables, "weighted", eps, group, scored) for group in GROUPS
            }
    run.write_stage(
        "O7",
        {
            **base,
            "status": "EVALUATED",
            "sigma": sigma_rows,
            "fits": [
                {
                    "fold": row["fold"],
                    "scored": row["scored"],
                    "fit_prefix_count": len(row["fit_prefixes"]),
                    "eval_prefix_count": len(row["eval_prefixes"]),
                    "B_sha256": row["B_sha256"],
                    "B_mu_sha256": row["B_mu_sha256"],
                    "B_rank": row["B_report"],
                    "B_mu_rank": row["B_mu_report"],
                }
                for row in fold_rows
            ],
            "reachable_forecast_disagreement": disagreement_public,
            "pooled_over_scored_folds": pooled,
            "unresolved_folds": unresolved_folds,
            "coverage": _coverage_report(tables, scored, unresolved_folds),
            "guard_failing_phi": guard_failures,
        },
    )


def _principal_angle(matrix: np.ndarray) -> dict:
    marginal = matrix[:, :2]
    kappa = matrix[:, 2]
    if float(np.linalg.norm(kappa)) == 0.0 or float(np.linalg.norm(marginal)) == 0.0:
        return {"radians": None, "reason": "undefined"}
    u_factor, values, _vh = np.linalg.svd(marginal, full_matrices=False)
    keep = values > 0.0
    if not np.any(keep):
        return {"radians": None, "reason": "undefined"}
    basis = u_factor[:, keep]
    projected = basis @ (basis.T @ kappa)
    cosine = float(np.linalg.norm(projected) / np.linalg.norm(kappa))
    cosine = float(min(1.0, max(-1.0, cosine)))
    return {"radians": float(math.acos(cosine))}


def stage_o3(run, ctx: dict) -> None:
    run.check_deadline("O3")
    rows = []
    group_rows = {"MARG": (0, 1), "XOR": (2,), "ALL": (0, 1, 2)}
    for prefix in range(16):
        entry = {"prefix": prefix, "groups": {}}
        for group, indexes in group_rows.items():
            blocks = [ctx["L"][(prefix, continuation)][list(indexes), :] for continuation in range(16)]
            stacked = np.vstack(blocks)
            values = singular_values(stacked)
            entry["groups"][group] = {
                "shape": [int(stacked.shape[0]), int(stacked.shape[1])],
                "singular_values": [float(value) for value in values],
                "principal_angle_kappa_vs_marginal_columns": _principal_angle(stacked),
            }
        rows.append(entry)
    run.write_stage("O3", {"status": "DESCRIPTIVE", "per_prefix": rows})


def stage_o4(run, ctx: dict, draws: dict) -> None:
    run.check_deadline("O4")
    sd = ctx["sd"]
    sizes = []
    for size in O4_SIZES:
        n_valid = 0
        n_total = 0
        per_prefix = []
        for prefix in range(16):
            valid = 0
            total = 0
            theta = ctx["theta"][prefix]
            for direction in draws["O4_directions"]:
                step = float(size) * sd * direction
                for sign in (1.0, -1.0):
                    belief = world.inverse_chart_float(theta + sign * step)
                    total += 1
                    if _valid(belief):
                        valid += 1
            per_prefix.append({"prefix": prefix, "n_valid": valid, "n_total": total})
            n_valid += valid
            n_total += total
        sizes.append(
            {
                "s": size,
                "n_valid": n_valid,
                "n_total": n_total,
                "per_prefix": per_prefix,
                "invalid_counted_in_denominator": True,
            }
        )
    run.write_stage("O4", {"status": "DESCRIPTIVE", "float_propagations": 0, "sizes": sizes})


def _o5_exclude(totals, size, weight: float, kind: str) -> None:
    for group in GROUPS:
        row = totals[(size, group)]
        row[kind + "_count"] += 1
        row[kind + "_law_mass"] += weight


def stage_o5(run, ctx: dict, draws: dict) -> None:
    """O4 validity on both charts, one common mask, before Phi. Descriptive only."""
    run.check_deadline("O5")
    sd = ctx["sd"]
    totals = {
        (size, group): {
            "contrast": 0.0,
            "response": 0.0,
            "denominator": 0.0,
            "n": 0,
            "invalid_count": 0,
            "invalid_law_mass": 0.0,
            "value_error_count": 0,
            "value_error_law_mass": 0.0,
            "non_finite_count": 0,
            "non_finite_law_mass": 0.0,
        }
        for size in O4_SIZES
        for group in GROUPS
    }
    for prefix in range(16):
        theta = ctx["theta"][prefix]
        for continuation in range(16):
            q_base, _belief = run.phi_cached(("true", prefix, continuation), theta, continuation, "true_baseline")
            weight = ctx["P_h"][(prefix, continuation)]
            for direction_index, direction in enumerate(draws["O4_directions"]):
                step = sd * direction
                for sign in (1.0, -1.0):
                    for size in O4_SIZES:
                        delta = sign * float(size) * step
                        delta_kappa0 = delta.copy()
                        delta_kappa0[2] = 0.0
                        theta_pert = theta + delta
                        theta_zero = theta + delta_kappa0
                        if not (
                            _valid(world.inverse_chart_float(theta_pert))
                            and _valid(world.inverse_chart_float(theta_zero))
                        ):
                            _o5_exclude(totals, size, weight, "invalid")
                            continue
                        q_pert = None
                        q_zero = None
                        failure = None
                        try:
                            q_pert, _belief = run.phi(
                                theta_pert,
                                continuation,
                                "O5",
                                ("O5", prefix, continuation, direction_index, sign, size, "pert"),
                            )
                        except ValueError:
                            failure = "value_error"
                        if failure is None:
                            try:
                                q_zero, _belief = run.phi(
                                    theta_zero,
                                    continuation,
                                    "O5",
                                    ("O5", prefix, continuation, direction_index, sign, size, "kappa0"),
                                )
                            except ValueError:
                                failure = "value_error"
                        if failure is not None:
                            _o5_exclude(totals, size, weight, failure)
                            continue
                        if not (
                            np.all(np.isfinite(q_pert))
                            and np.all(np.isfinite(q_zero))
                            and np.all(np.isfinite(q_base))
                        ):
                            _o5_exclude(totals, size, weight, "non_finite")
                            continue
                        contrast = q_pert - q_zero
                        response = q_pert - q_base
                        for group in GROUPS:
                            row = totals[(size, group)]
                            row["contrast"] += weight * squared_error(contrast, group)
                            row["response"] += weight * squared_error(response, group)
                            row["denominator"] += weight
                            row["n"] += 1
    report_rows = []
    for size in O4_SIZES:
        groups = {}
        for group in GROUPS:
            row = totals[(size, group)]
            excluded = {
                "invalid": {"count": row["invalid_count"], "law_mass": row["invalid_law_mass"]},
                "value_error": {"count": row["value_error_count"], "law_mass": row["value_error_law_mass"]},
                "non_finite": {"count": row["non_finite_count"], "law_mass": row["non_finite_law_mass"]},
            }
            if row["denominator"] == 0.0:
                groups[group] = {
                    "H": None,
                    "response_energy": None,
                    "R": "UNDEFINED",
                    "denominator": 0.0,
                    "n": 0,
                    "excluded": excluded,
                }
            else:
                contrast = row["contrast"] / row["denominator"]
                response = row["response"] / row["denominator"]
                groups[group] = {
                    "H": contrast,
                    "response_energy": response,
                    "R": "UNDEFINED" if response == 0.0 else contrast / response,
                    "denominator": row["denominator"],
                    "n": row["n"],
                    "excluded": excluded,
                }
        report_rows.append(
            {
                "s": size,
                "groups": groups,
                "descriptive_only": True,
                "probability_guard_applied": True,
                "common_mask": True,
            }
        )
    run.write_stage("O5", {"status": "DESCRIPTIVE", "sizes": report_rows})
