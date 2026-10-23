"""Stage S6. Per-system baselines and finite edits, with streaming checks (E39-3)."""

from __future__ import annotations

import numpy as np

from ckappa_oracle.geometry import squared_error
from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_oracle.pinned import FROZEN_RUNTIME, fnum
from ckappa_oracle.world import inverse_chart_float
from ckappa_classfit.classes import CLASS_ORDER, GROUPS, ORBITS, class_of_prefix, folds
from ckappa_classfit.pinned import SYSTEM_ORDER, TRUE_CHART_SYSTEMS
from ckappa_classfit.rankcats import category_blocks_propagation, recovery_ok, skip_reason, zero_gain_ok
from ckappa_classfit.schedule import EDITS_PER_FOLD_SIZE

GUARD = fnum("guard")
EPS = tuple(FROZEN_RUNTIME["eps_syn"])
RECOVERY = 1e-9


def _sign_pm(value: float) -> int:
    if value > 0.0:
        return 1
    if value < 0.0:
        return -1
    return 0


def _pipeline(reason: str, exit_code: int, **detail):
    payload = {"reason": reason, "diagnosis": "operational failure"}
    payload.update(detail)
    raise PackageStop("PIPELINE INVALID", exit_code, payload)


def _valid(belief: np.ndarray) -> bool:
    return bool(np.all(np.asarray(belief, dtype=np.float64) >= GUARD))


def _min_p(belief: np.ndarray) -> float:
    return float(np.min(belief))


def _pad_mu(matrix: np.ndarray | None) -> np.ndarray | None:
    if matrix is None:
        return None
    full = np.zeros((3, matrix.shape[1]), dtype=np.float64)
    full[:2, :] = matrix
    return full


def _crosses_pc(psi: np.ndarray, prime: np.ndarray) -> bool:
    for index in (0, 1):
        if prime[index] == 0.0 or _sign_pm(prime[index]) != _sign_pm(psi[index]):
            return True
    return False


def _crosses_lim(psi: np.ndarray, prime: np.ndarray, threshold: float) -> bool:
    if abs(float(prime[0])) == threshold:
        return True
    return _sign_pm(abs(float(prime[0])) - threshold) != _sign_pm(abs(float(psi[0])) - threshold)


def _actual_chart(system, prefix, delta):
    name = system["name"]
    base = system["baseline"][prefix]
    if name == "SYS-PC":
        psi = system["psi"][prefix]
        prime = psi + system["C"] @ delta
        return base + system["slope"][prefix] @ delta, _crosses_pc(psi, prime), prime
    if name == "SYS-LIM":
        psi = system["psi"][prefix]
        prime = psi + system["C"] @ delta
        return base + system["slope"][prefix] @ delta, _crosses_lim(psi, prime, system["t_float"]), prime
    if name == "SYS-FK":
        return base + system["C_full"] @ delta, False, None
    if name == "SYS-NC1":
        from ckappa_oracle.geometry import g_value

        mu_prime = base[:2] + system["C_mu"] @ delta
        theta = np.array([mu_prime[0], mu_prime[1], g_value(system_coef(system), float(mu_prime[0]), float(mu_prime[1]))], dtype=np.float64)
        return theta, False, None
    if name == "SYS-NC2":
        mu_prime = base[:2] + system["C_mu"] @ delta
        theta = np.array([mu_prime[0], mu_prime[1], system["c2"] * float(mu_prime[0])], dtype=np.float64)
        return theta, False, None
    if name == "SYS-NC3":
        mu_prime = base[:2] + system["C_mu"] @ delta
        mx = float(mu_prime[0])
        theta = np.array([mx, mu_prime[1], system["c3"] * mx * mx * mx], dtype=np.float64)
        return theta, False, None
    return base + system["B_true"] @ delta, False, None


def system_coef(system):
    return system["nc1_coef"]


def _propagate(run, system_name, theta, continuation, key):
    before = run.float_count
    try:
        forecast, belief = run.phi(theta, continuation, "S6", key)
    except PackageStop:
        if run.float_count > before:
            run.ledger.add(system_name, "S6", "propagation", "ATTEMPTED", 1, "valid_finite")
        raise
    except ValueError as exc:
        run.ledger.add(system_name, "S6", "propagation", "ATTEMPTED", 1, "value_error")
        return None, None, "value_error", str(exc)
    if not np.all(np.isfinite(forecast)):
        run.ledger.add(system_name, "S6", "propagation", "ATTEMPTED", 1, "non_finite")
        return None, belief, "non_finite", None
    run.ledger.add(system_name, "S6", "propagation", "ATTEMPTED", 1, "valid_finite")
    return forecast, belief, "valid_finite", None


def _blank_loss():
    return {"mu": 0.0, "full": 0.0, "S": 0.0, "den": 0.0, "n": 0, "n_scoreable": 0, "mass_s": 0.0, "mass_t": 0.0, "n_total": 0}


def _blank_cov():
    return {"n_scoreable": 0, "n_total": 0, "mass_s": 0.0, "mass_t": 0.0, "crossings": 0}


class _Cell:
    def __init__(self):
        self.n_tested = 0
        self.max_abs = None
        self.worst = None
        self.n_stop = 0
        self.n_reverse = 0
        self.n_actual_valid = 0
        self.first = None


def stage_s6(run, ctx, draws) -> None:
    run.check_deadline("S6")
    directions = draws["O6_directions"]
    orbit_of = ctx["orbit_of"]
    class_of = ctx["class_of"]
    for system_name in SYSTEM_ORDER:
        run.check_deadline(f"S6 {system_name}")
        system = ctx["systems"][system_name]
        system["name"] = system_name
        if system_name == "SYS-NC1":
            system["nc1_coef"] = ctx["nc1_coef"]
        if system_name == "SYS-NC2":
            system["c2"] = ctx["c2"]
        if system_name == "SYS-NC3":
            system["c3"] = ctx["c3"]
        if not system["admissible"]:
            payload = {
                "system": system_name,
                "system_inadmissible": True,
                "loss_records": [],
                "coverage": [],
                "identities": [],
                "guard_consistency": [],
                "crossings": 0,
            }
            ctx.setdefault("evaluations", {})[system_name] = payload
            run.write_json(f"eval_{system_name}.json", payload)
            run.checkpoint(f"S6 {system_name}")
            continue
        _evaluate_system(run, ctx, system, directions, orbit_of, class_of)


def _evaluate_system(run, ctx, system, directions, orbit_of, class_of) -> None:
    name = system["name"]
    baseline_q = {}
    baseline_gap = None
    for prefix in range(16):
        if prefix in system["voids"]:
            run.ledger.add(name, "S6", "propagation", "SKIPPED_PREFIX_VOID", 16)
            continue
        for continuation in range(16):
            theta = system["baseline"][prefix]
            key = (name, "baseline", prefix, continuation)
            forecast, _belief, kind, error = _propagate(run, name, theta, continuation, key)
            if kind == "value_error":
                _pipeline("baseline propagation", 2, system=name, prefix=prefix, continuation=continuation, error=error)
            if kind == "non_finite":
                _pipeline("baseline propagation", 2, system=name, prefix=prefix, continuation=continuation, failure="non-finite")
            baseline_q[(prefix, continuation)] = forecast
            if name in TRUE_CHART_SYSTEMS:
                exact = ctx["forecasts_exact"][prefix + 16 * continuation]
                exact_q = np.array([float(exact[0]), float(exact[1]), float(exact[2])], dtype=np.float64)
                gap = float(np.max(np.abs(forecast - exact_q)))
                baseline_gap = gap if baseline_gap is None else max(baseline_gap, gap)
    losses = {}
    coverage = {}
    finite = {}
    guards = {}
    _prepare_identity_slots(name, system, finite, guards)
    for fold_name, _fit, evaluation in folds():
        run.check_deadline(f"S6 {name} {fold_name}")
        for prefix in evaluation:
            orbit = orbit_of[prefix]
            klass = class_of[prefix]
            for continuation in range(16):
                weight = float(ctx["P_h"][(prefix, continuation)])
                q_base = None if prefix in system["voids"] else baseline_q[(prefix, continuation)]
                for direction_index in range(16):
                    direction = directions[direction_index]
                    for sign in (1.0, -1.0):
                        for eps in EPS:
                            _one_edit(
                                run, ctx, system, fold_name, prefix, continuation, direction_index,
                                direction, sign, eps, weight, q_base, orbit, klass, losses, coverage,
                                finite, guards, 
                            )
        _zero_gain_fold(name, system, fold_name, losses, finite)
        run.checkpoint(f"S6 {name} {fold_name}")
    for fold_name, _fit, _evaluation in folds():
        for eps in EPS:
            row = coverage[(fold_name, None, eps)]
            if row["n_total"] != EDITS_PER_FOLD_SIZE:
                integrity_stop("edit-count mismatch", system=name, fold=fold_name, eps_syn=eps, n_total=row["n_total"])
    crossings = 0
    for (fold_name, klass, _eps), row in coverage.items():
        if klass is None:
            crossings += row["crossings"]
    payload = {
        "system": name,
        "system_inadmissible": False,
        "loss_records": _emit_losses(name, system, losses),
        "coverage": _emit_coverage(name, coverage),
        "identities": _emit_finite(name, system, finite),
        "guard_consistency": _emit_guards(name, guards),
        "crossings": crossings,
        "baseline_vs_o1_max_abs": baseline_gap,
        "baseline_vs_o1_note": "reported check; no frozen tolerance is declared for this comparison",
        "d6_d7": [row for row in system.get("matrix_identities", []) if str(row["identity_id"]).startswith("D6") or str(row["identity_id"]).startswith("D7")],
        "accounting": [row for row in run.ledger.records() if row["system"] == name],
    }
    ctx.setdefault("evaluations", {})[name] = payload
    run.write_json(f"eval_{name}.json", payload)
    run.checkpoint(f"S6 {name}")
    run.log(f"eval {name} written")


def _prepare_identity_slots(name, system, finite, guards) -> None:
    fold_names = [row[0] for row in folds()]
    if name == "SYS-O6":
        for fold in fold_names:
            for eps in EPS:
                finite[("rec", "global", fold, None, eps, "global_full")] = _Cell()
                guards[("global_full", "global", fold, None, eps)] = _Cell()
                for klass in CLASS_ORDER:
                    finite[("rec", "class", fold, klass, eps, "class_full")] = _Cell()
                    guards[("class_full", "class", fold, klass, eps)] = _Cell()
    elif name == "SYS-PC":
        for fold in fold_names:
            for eps in EPS:
                finite[("eq", "global", fold, None, eps, "global")] = _Cell()
                for klass in CLASS_ORDER:
                    finite[("rec", "class", fold, klass, eps, "class_full")] = _Cell()
                    guards[("class_full", "class", fold, klass, eps)] = _Cell()
            for eps in EPS:
                for group in GROUPS:
                    finite[("gain", "global", fold, None, eps, group)] = _Cell()
    elif name == "SYS-FK":
        for fold in fold_names:
            for eps in EPS:
                for predictor, fit_type, klass in (
                    ("global_full", "global", None),
                    ("global_mu", "global", None),
                ):
                    finite[("rec", fit_type, fold, klass, eps, predictor)] = _Cell()
                    guards[(predictor, fit_type, fold, klass, eps)] = _Cell()
                for klass in CLASS_ORDER:
                    for predictor in ("class_full", "class_mu"):
                        finite[("rec", "class", fold, klass, eps, predictor)] = _Cell()
                        guards[(predictor, "class", fold, klass, eps)] = _Cell()
                for group in GROUPS:
                    finite[("gain", "global", fold, None, eps, group)] = _Cell()
                    for klass in CLASS_ORDER:
                        finite[("gain", "class", fold, klass, eps, group)] = _Cell()
    elif name == "SYS-NC1":
        for fold in fold_names:
            for eps in EPS:
                for group in GROUPS:
                    finite[("gain", "global", fold, None, eps, group)] = _Cell()


def _map_category(system, fold, key, which):
    slot = system["maps"][fold][key]
    return slot["full_category"] if which == "full" else slot["mu_category"]


def _map_matrix(system, fold, key, which):
    slot = system["maps"][fold][key]
    if which == "full":
        return slot["full"]
    return _pad_mu(slot["mu"])


def _one_edit(run, ctx, system, fold, prefix, continuation, direction_index, direction, sign, eps, weight, q_base, orbit, klass, losses, coverage, finite, guards):
    name = system["name"]
    void = prefix in system["voids"]
    _touch_coverage(coverage, fold, klass, eps, weight, False, void_only=void)
    _touch_loss_totals(losses, name, fold, klass, orbit, eps, weight)
    if void:
        run.ledger.add(name, "S6", "propagation", "SKIPPED_PREFIX_VOID", 5)
        return
    delta = float(eps) * float(sign) * np.asarray(direction, dtype=np.float64)
    theta_actual, crossed, _prime = _actual_chart(system, prefix, delta)
    if crossed:
        coverage[(fold, None, eps)]["crossings"] += 1
        coverage[(fold, klass, eps)]["crossings"] += 1
        from ckappa_oracle.io import integrity_stop as _stop

        _stop("observed crossing", system=name, fold=fold, prefix=prefix, continuation=continuation, direction=direction_index, sign=sign, eps_syn=eps)
    predictions = {
        "global_full": _map_matrix(system, fold, "global", "full"),
        "global_mu": _map_matrix(system, fold, "global", "mu"),
        "class_full": _map_matrix(system, fold, klass, "full"),
        "class_mu": _map_matrix(system, fold, klass, "mu"),
    }
    categories = {
        "global_full": _map_category(system, fold, "global", "full"),
        "global_mu": _map_category(system, fold, "global", "mu"),
        "class_full": _map_category(system, fold, klass, "full"),
        "class_mu": _map_category(system, fold, klass, "mu"),
    }
    thetas = {"actual": theta_actual}
    for pred_name, matrix in predictions.items():
        thetas[pred_name] = None if matrix is None else system["baseline"][prefix] + matrix @ delta
    beliefs = {}
    for pred_name, theta in thetas.items():
        if theta is None:
            beliefs[pred_name] = None
        else:
            beliefs[pred_name] = inverse_chart_float(theta)
    scoreable = all(beliefs[key] is not None and _valid(beliefs[key]) for key in ("actual", "global_full", "global_mu", "class_full", "class_mu"))
    if name in ("SYS-PC", "SYS-LIM"):
        scoreable = scoreable and not crossed
    forecasts = {}
    kinds = {}
    for pred_name in ("actual", "global_full", "global_mu", "class_full", "class_mu"):
        unavailable = pred_name != "actual" and category_blocks_propagation(categories[pred_name])
        reason = skip_reason(
            stopped=run.stopped,
            system_inadmissible=False,
            prefix_void=False,
            map_unavailable=unavailable,
        )
        if reason is not None:
            run.ledger.add(name, "S6", "propagation", reason, 1)
            forecasts[pred_name] = None
            kinds[pred_name] = reason
            continue
        key = (name, fold, prefix, continuation, direction_index, sign, eps, pred_name)
        forecast, _belief, kind, error = _propagate(run, name, thetas[pred_name], continuation, key)
        forecasts[pred_name] = forecast
        kinds[pred_name] = kind
        if scoreable and kind in ("value_error", "non_finite"):
            _pipeline("scoreable edit", 2, system=name, failure=kind, error=error, edit=list(key))
    _streaming(name, system, fold, prefix, continuation, direction_index, sign, eps, klass, beliefs, forecasts, thetas, categories, scoreable, finite, guards)
    if not scoreable or any(forecasts[key] is None for key in forecasts):
        return
    actual = forecasts["actual"] - q_base
    pieces = {
        "global": (forecasts["global_mu"] - q_base, forecasts["global_full"] - q_base),
        "class": (forecasts["class_mu"] - q_base, forecasts["class_full"] - q_base),
    }
    for group in GROUPS:
        se_actual = squared_error(actual, group)
        for fit_type, (pred_mu, pred_full) in pieces.items():
            se_mu = squared_error(actual - pred_mu, group)
            se_full = squared_error(actual - pred_full, group)
            for mode, factor in (("weighted", weight), ("unweighted", 1.0)):
                row = losses[(fit_type, fold, klass, orbit, group, eps, mode)]
                row["mu"] += factor * se_mu
                row["full"] += factor * se_full
                row["S"] += factor * se_actual
                row["den"] += factor
                row["n"] += 1
                row["n_scoreable"] += 1
                row["mass_s"] += weight
    coverage[(fold, None, eps)]["n_scoreable"] += 1
    coverage[(fold, None, eps)]["mass_s"] += weight
    coverage[(fold, klass, eps)]["n_scoreable"] += 1
    coverage[(fold, klass, eps)]["mass_s"] += weight


def _touch_coverage(coverage, fold, klass, eps, weight, scoreable, void_only=False):
    for key in ((fold, None, eps), (fold, klass, eps)):
        row = coverage.setdefault(key, _blank_cov())
        row["n_total"] += 1
        row["mass_t"] += weight
        if scoreable:
            row["n_scoreable"] += 1
            row["mass_s"] += weight


def _touch_loss_totals(losses, name, fold, klass, orbit, eps, weight):
    for fit_type in ("global", "class"):
        for group in GROUPS:
            for mode in ("weighted", "unweighted"):
                row = losses.setdefault((fit_type, fold, klass, orbit, group, eps, mode), _blank_loss())
                row["n_total"] += 1
                row["mass_t"] += weight


def _streaming(name, system, fold, prefix, continuation, direction_index, sign, eps, klass, beliefs, forecasts, thetas, categories, scoreable, finite, guards):
    actual_ok = beliefs["actual"] is not None and _valid(beliefs["actual"])
    if name == "SYS-O6":
        _recovery(name, system, finite, guards, "global", fold, None, eps, "global_full", categories["global_full"], actual_ok, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign)
        _recovery(name, system, finite, guards, "class", fold, klass, eps, "class_full", categories["class_full"], actual_ok, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign)
    elif name == "SYS-PC":
        _equality(finite, fold, eps, categories, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign)
        _recovery(name, system, finite, guards, "class", fold, klass, eps, "class_full", categories["class_full"], actual_ok, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign)
    elif name == "SYS-FK":
        for predictor, fit_type, cell_class, category in (
            ("global_full", "global", None, categories["global_full"]),
            ("global_mu", "global", None, categories["global_mu"]),
            ("class_full", "class", klass, categories["class_full"]),
            ("class_mu", "class", klass, categories["class_mu"]),
        ):
            _recovery(name, system, finite, guards, fit_type, fold, cell_class, eps, predictor, category, actual_ok, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign)


def _guard_and_maybe_stop(guards, key, actual_ok, pred_ok, beliefs, thetas, forecasts, predictor, prefix, continuation, direction_index, sign, eps, category):
    if category != "FULL":
        return
    cell = guards[key]
    if actual_ok:
        cell.n_actual_valid += 1
        if not pred_ok:
            cell.n_stop += 1
            if cell.first is None:
                actual_q = forecasts.get("actual")
                pred_q = forecasts.get(predictor)
                residual = None
                if actual_q is not None and pred_q is not None:
                    residual = float(np.max(np.abs(actual_q - pred_q)))
                cell.first = {
                    "edit": {"prefix": prefix, "continuation": continuation, "direction": direction_index, "sign": sign, "eps_syn": eps},
                    "min_p_actual": _min_p(beliefs["actual"]),
                    "min_p_predicted": _min_p(beliefs[predictor]) if beliefs[predictor] is not None else None,
                    "chart_diff_max_abs": float(np.max(np.abs(thetas["actual"] - thetas[predictor]))) if thetas[predictor] is not None else None,
                    "recovery_residual_max_abs": residual,
                }
            detail = dict(cell.first)
            detail["description"] = "a guard inconsistency"
            detail["not"] = "proof that the recovery tolerance was exceeded"
            _pipeline("guard inconsistency", 7, **detail)
    elif pred_ok:
        cell.n_reverse += 1


def _recovery(name, system, finite, guards, fit_type, fold, klass, eps, predictor, category, actual_ok, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign):
    pred_ok = beliefs[predictor] is not None and _valid(beliefs[predictor])
    guard_key = (predictor, fit_type, fold, klass, eps)
    if guard_key in guards:
        _guard_and_maybe_stop(guards, guard_key, actual_ok, pred_ok, beliefs, thetas, forecasts, predictor, prefix, continuation, direction_index, sign, eps, category)
    if category != "FULL" or not actual_ok:
        return
    actual_q = forecasts.get("actual")
    pred_q = forecasts.get(predictor)
    if actual_q is None or pred_q is None:
        return
    cell = finite[("rec", fit_type, fold, klass, eps, predictor)]
    cell.n_tested += 1
    err = float(np.max(np.abs(actual_q - pred_q)))
    if cell.max_abs is None or err >= cell.max_abs:
        cell.max_abs = err
        cell.worst = {"prefix": prefix, "continuation": continuation, "direction": direction_index, "sign": sign, "eps_syn": eps}
    if not recovery_ok(err):
        _pipeline("finite recovery", 2, system=name, predictor=predictor, fold=fold, klass=klass, eps_syn=eps, max_abs=err, tolerance=RECOVERY, edit=cell.worst)


def _equality(finite, fold, eps, categories, beliefs, forecasts, thetas, prefix, continuation, direction_index, sign):
    both = (
        beliefs["global_full"] is not None
        and beliefs["global_mu"] is not None
        and _valid(beliefs["global_full"])
        and _valid(beliefs["global_mu"])
    )
    if not both:
        return
    if categories["global_full"] != "FULL" or categories["global_mu"] != "FULL":
        return
    q_full = forecasts.get("global_full")
    q_mu = forecasts.get("global_mu")
    if q_full is None or q_mu is None:
        return
    cell = finite[("eq", "global", fold, None, eps, "global")]
    cell.n_tested += 1
    err = float(np.max(np.abs(q_full - q_mu)))
    if cell.max_abs is None or err >= cell.max_abs:
        cell.max_abs = err
        cell.worst = {"prefix": prefix, "continuation": continuation, "direction": direction_index, "sign": sign, "eps_syn": eps}
    if not recovery_ok(err):
        _pipeline("SYS-PC global finite equality", 2, fold=fold, eps_syn=eps, max_abs=err, tolerance=RECOVERY, edit=cell.worst)


def _pool_loss(losses, fit_type, fold, klass, eps, group):
    """Sum a fold-level or fold-class cell across the orbits that belong to it."""
    total_mu = total_full = total_s = den = 0.0
    n_score = 0
    seen = False
    for key, row in losses.items():
        key_fit, key_fold, key_class, _orbit, key_group, key_eps, mode = key
        if mode != "weighted" or key_fit != fit_type or key_fold != fold or key_group != group or key_eps != eps:
            continue
        if klass is not None and key_class != klass:
            continue
        seen = True
        total_mu += row["mu"]
        total_full += row["full"]
        total_s += row["S"]
        den += row["den"]
        n_score += row["n_scoreable"]
    if not seen or n_score == 0 or den == 0.0:
        return None
    return total_mu / den, total_full / den, total_s / den, n_score


def _zero_gain_fold(name, system, fold, losses, finite):
    if name not in ("SYS-PC", "SYS-FK", "SYS-NC1"):
        return
    for eps in EPS:
        for group in GROUPS:
            if name in ("SYS-PC", "SYS-NC1", "SYS-FK"):
                _apply_gain(name, system, finite, losses, "global", fold, None, eps, group)
            if name == "SYS-FK":
                for klass in CLASS_ORDER:
                    _apply_gain(name, system, finite, losses, "class", fold, klass, eps, group)


def _gain_premise(system, fold, fit_type, klass):
    key = "global" if fit_type == "global" else klass
    slot = system["maps"][fold][key]
    if slot["full_category"] == "UNAVAILABLE_EMPTY" or slot["mu_category"] == "UNAVAILABLE_EMPTY":
        return "UNAVAILABLE_EMPTY"
    if slot["full_category"] == "UNRESOLVED" or slot["mu_category"] == "UNRESOLVED":
        return "UNRESOLVED"
    if slot["full_category"] != "FULL" or slot["mu_category"] != "FULL":
        return "LOWER" if "LOWER" in (slot["full_category"], slot["mu_category"]) or "ZERO_NONEMPTY" in (slot["full_category"], slot["mu_category"]) else slot["full_category"]
    if system["name"] == "SYS-NC1" and system["voids"]:
        return "VOIDS"
    return "FULL"


def _apply_gain(name, system, finite, losses, fit_type, fold, klass, eps, group):
    key = ("gain", fit_type, fold, klass, eps, group)
    if key not in finite:
        return
    cell = finite[key]
    premise = _gain_premise(system, fold, fit_type, klass)
    pooled = _pool_loss(losses, fit_type, fold, klass, eps, group)
    if premise != "FULL":
        cell.n_tested = 0
        cell.max_abs = None
        cell.worst = {"premise": premise}
        return
    if pooled is None:
        cell.n_tested = 0
        return
    loss_mu, loss_full, response, n_score = pooled
    diff = abs(loss_mu - loss_full)
    cell.n_tested = n_score
    cell.max_abs = diff
    cell.worst = {"S": response, "L_mu": loss_mu, "L_full": loss_full}
    if name == "SYS-NC1":
        return
    if not zero_gain_ok(loss_mu, loss_full, response):
        _pipeline(
            "zero-gain identity",
            2,
            system=name,
            fit_type=fit_type,
            fold=fold,
            klass=klass,
            group=group,
            eps_syn=eps,
            absolute_difference=diff,
            scale=response,
            tolerance=1e-18 + 1e-9 * response,
        )


def _emit_losses(name, system, losses):
    rows = []
    orbits = ORBITS
    for fit_type in ("global", "class"):
        for fold_name, _fit, evaluation in folds():
            for klass in CLASS_ORDER:
                for prefix in evaluation:
                    if class_of_prefix()[prefix] != klass:
                        continue
                    orbit = None
                    for orbit_name, members in orbits.items():
                        if prefix in members:
                            orbit = orbit_name
                    for group in GROUPS:
                        for eps in EPS:
                            for mode in ("weighted", "unweighted"):
                                row = losses.get((fit_type, fold_name, klass, orbit, group, eps, mode))
                                formed = _loss_formed(system, fold_name, fit_type, klass)
                                if row is None or not formed or row["n_scoreable"] == 0 or row["den"] == 0.0:
                                    rows.append(
                                        {
                                            "system": name,
                                            "fit_type": fit_type,
                                            "fold": fold_name,
                                            "class": klass,
                                            "eval_orbit": orbit,
                                            "group": group,
                                            "eps_syn": eps,
                                            "mode": mode,
                                            "L_mu": None,
                                            "L_full": None,
                                            "S": None,
                                            "gain": None,
                                            "n_scoreable": None if row is None or not formed else row["n_scoreable"],
                                            "n_total": None if row is None else row["n_total"],
                                            "law_mass_scoreable": None if row is None or not formed else row["mass_s"],
                                            "law_mass_total": None if row is None else row["mass_t"],
                                        }
                                    )
                                    continue
                                loss_mu = row["mu"] / row["den"]
                                loss_full = row["full"] / row["den"]
                                response = row["S"] / row["den"]
                                rows.append(
                                    {
                                        "system": name,
                                        "fit_type": fit_type,
                                        "fold": fold_name,
                                        "class": klass,
                                        "eval_orbit": orbit,
                                        "group": group,
                                        "eps_syn": eps,
                                        "mode": mode,
                                        "L_mu": loss_mu,
                                        "L_full": loss_full,
                                        "S": response,
                                        "gain": loss_mu - loss_full,
                                        "n_scoreable": row["n_scoreable"],
                                        "n_total": row["n_total"],
                                        "law_mass_scoreable": row["mass_s"],
                                        "law_mass_total": row["mass_t"],
                                    }
                                )
    return rows


def _loss_formed(system, fold, fit_type, klass) -> bool:
    """Common mask needs all four maps. Any blocking map leaves the comparison unformed."""
    global_slot = system["maps"][fold]["global"]
    class_slot = system["maps"][fold][klass]
    cats = (
        global_slot["full_category"],
        global_slot["mu_category"],
        class_slot["full_category"],
        class_slot["mu_category"],
    )
    return not any(category_blocks_propagation(cat) for cat in cats)


def _emit_coverage(name, coverage):
    rows = []
    for (fold, klass, eps), row in sorted(coverage.items(), key=lambda item: (item[0][0], "" if item[0][1] is None else item[0][1], item[0][2])):
        mass = None if row["mass_t"] == 0.0 else row["mass_s"] / row["mass_t"]
        count_pass = not (4 * row["n_scoreable"] < 3 * row["n_total"])
        mass_pass = mass is not None and not (mass < 0.75 * (1.0 - 1e-6))
        rows.append(
            {
                "system": name,
                "fold": fold,
                "class": klass,
                "eps_syn": eps,
                "n_total": row["n_total"],
                "n_scoreable": row["n_scoreable"],
                "law_mass_total": row["mass_t"],
                "law_mass_scoreable": row["mass_s"],
                "count_rule_pass": count_pass,
                "mass_rule_pass": mass_pass,
                "crossings": row["crossings"],
            }
        )
    return rows


def _emit_finite(name, system, finite):
    rows = []
    for key, cell in finite.items():
        kind_tag, fit_type, fold, klass, eps, extra = key
        if kind_tag == "rec":
            kind = "finite_recovery"
            group = None
            predictor = extra
        elif kind_tag == "eq":
            kind = "finite_equality"
            group = None
            predictor = extra
        else:
            kind = "zero_gain"
            group = extra
            predictor = None
        category = _finite_category(system, fold, fit_type, klass, kind_tag, predictor)
        status = _finite_status(name, kind_tag, category, cell)
        rows.append(
            {
                "system": name,
                "identity_id": f"{name}-{kind}-{fit_type}-{fold}-{klass}-{group}-{eps}-{predictor}",
                "kind": kind,
                "fit_type": fit_type,
                "fold": fold,
                "class": klass,
                "group": group,
                "eps_syn": eps,
                "premise_rank_category": category,
                "status": status,
                "max_abs_residual": cell.max_abs,
                "tolerance_abs": 1e-9 if kind != "zero_gain" else 1e-18,
                "tolerance_rel": 0.0 if kind != "zero_gain" else 1e-9,
                "scale": None if not isinstance(cell.worst, dict) else cell.worst.get("S"),
                "n_tested": cell.n_tested,
                "worst_edit": cell.worst,
            }
        )
    return rows


def _finite_category(system, fold, fit_type, klass, kind_tag, predictor):
    key = "global" if fit_type == "global" or klass is None else klass
    slot = system["maps"][fold][key]
    if kind_tag == "rec":
        if predictor is not None and "mu" in predictor:
            return slot["mu_category"]
        return slot["full_category"]
    if kind_tag == "eq":
        return _gain_premise(system, fold, "global", None)
    return _gain_premise(system, fold, fit_type, klass)


def _finite_status(name, kind_tag, category, cell):
    if category == "UNAVAILABLE_EMPTY":
        return "UNAVAILABLE"
    if category == "UNRESOLVED":
        return "REFERENCE_RANK_UNRESOLVED"
    if category in ("LOWER", "ZERO_NONEMPTY"):
        return "NOT_APPLICABLE_RANK"
    if category == "VOIDS":
        return "NOT_APPLICABLE_VOIDS"
    if cell.n_tested == 0:
        return "NOT_EVALUATED"
    if kind_tag == "gain" and name == "SYS-NC1":
        return "PASS" if cell.max_abs is not None and zero_gain_ok(cell.worst["L_mu"], cell.worst["L_full"], cell.worst["S"]) else "FAIL"
    if cell.max_abs is None:
        return "NOT_EVALUATED"
    if kind_tag == "gain":
        return "PASS" if zero_gain_ok(cell.worst["L_mu"], cell.worst["L_full"], cell.worst["S"]) else "FAIL"
    return "PASS" if recovery_ok(cell.max_abs) else "FAIL"


def _emit_guards(name, guards):
    rows = []
    for key, cell in guards.items():
        predictor, fit_type, fold, klass, eps = key
        rows.append(
            {
                "system": name,
                "predictor": predictor,
                "fit_type": fit_type,
                "fold": fold,
                "class": klass,
                "eps_syn": eps,
                "n_actual_valid_tested": cell.n_actual_valid,
                "n_stop_mismatch": cell.n_stop,
                "n_reverse_mismatch_recorded": cell.n_reverse,
                "first_mismatch": cell.first,
            }
        )
    return rows
