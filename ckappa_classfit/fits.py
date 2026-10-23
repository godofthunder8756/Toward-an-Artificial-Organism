"""Stage S5. Response-map fits, ranks, matrix identities, and fit freeze.

No fit in this stage runs before stage S4 has returned (driver order).
"""

from __future__ import annotations

import math

import numpy as np

from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_oracle.linalg_fit import fit_from_svd
from ckappa_classfit.classes import CLASS_ORDER, D7_FOLDS, FOLD_SPEC, ORBITS, folds
from ckappa_classfit.pinned import B3_SYSTEMS
from ckappa_classfit.rankcats import b3_status, cancellation_tolerance, rank_category_from_ratios
from ckappa_classfit.records import diag3, matrix_record, max_abs

RECOVERY = 1e-9


def _fail_identity(reason: str, **detail):
    payload = {"reason": reason, "diagnosis": "operational failure"}
    payload.update(detail)
    raise PackageStop("PIPELINE INVALID", 2, payload)


def _design(prefixes, columns, ell, jay, weights, voids):
    design_rows = []
    target_rows = []
    used = []
    for prefix in prefixes:
        if prefix in voids:
            continue
        used.append(prefix)
        for continuation in range(16):
            local_l = ell[(prefix, continuation)]
            local_j = jay[(prefix, continuation)]
            scale = math.sqrt(float(weights[(prefix, continuation)]))
            block = local_l if columns == 3 else local_l[:, :2]
            design_rows.append(scale * block)
            target_rows.append(scale * local_j)
    if not design_rows:
        return None, None, used
    return np.vstack(design_rows), np.vstack(target_rows), used


def _sum_normal(prefixes, gee, arr, voids):
    gram = np.zeros((3, 3), dtype=np.float64)
    rhs = np.zeros((3, 8), dtype=np.float64)
    used = []
    for prefix in prefixes:
        if prefix in voids or prefix not in gee:
            continue
        gram += gee[prefix]
        rhs += arr[prefix]
        used.append(prefix)
    return gram, rhs, used


def _term(system, scope, ident, name, matrix):
    packed = matrix_record(matrix)
    return {
        "system": system,
        "scope": scope,
        "id": ident,
        "name": name,
        "values": packed["values"],
        "sha256": packed["sha256"],
    }


def _identity(system, identity_id, kind, fit_type, fold, klass, group, eps, category, status, residual, n_tested, worst):
    return {
        "system": system,
        "identity_id": identity_id,
        "kind": kind,
        "fit_type": fit_type,
        "fold": fold,
        "class": klass,
        "group": group,
        "eps_syn": eps,
        "premise_rank_category": category,
        "status": status,
        "max_abs_residual": residual,
        "tolerance_abs": RECOVERY if status in ("PASS", "FAIL", "INVESTIGATE") or residual is not None else None,
        "tolerance_rel": 0.0,
        "scale": None,
        "n_tested": n_tested,
        "worst_edit": worst,
    }


def _joint_category(left: str, right: str) -> str:
    order = ("UNAVAILABLE_EMPTY", "UNRESOLVED", "ZERO_NONEMPTY", "LOWER", "FULL")
    # The blocking category wins. LOWER and ZERO both withhold the identity.
    rank = {
        "UNAVAILABLE_EMPTY": 0,
        "UNRESOLVED": 1,
        "ZERO_NONEMPTY": 2,
        "LOWER": 2,
        "FULL": 3,
    }
    if rank[left] <= rank[right]:
        return left
    return right


def _status_for(category: str, residual: float | None, *, stop: bool, investigate: bool):
    if category == "UNAVAILABLE_EMPTY":
        return "UNAVAILABLE", 0, False
    if category == "UNRESOLVED":
        return "REFERENCE_RANK_UNRESOLVED", 0, False
    if category in ("LOWER", "ZERO_NONEMPTY"):
        return "NOT_APPLICABLE_RANK", 0, False
    if category != "FULL" or residual is None:
        return "NOT_EVALUATED", 0, False
    if residual <= RECOVERY:
        return "PASS", 1, False
    if investigate:
        return "INVESTIGATE", 1, False
    return "FAIL", 1, stop


def _apply_check(records, system, identity_id, fit_type, fold, klass, category, residual, *, stop: bool, investigate: bool = False):
    status, n_tested, failing = _status_for(category, residual, stop=stop, investigate=investigate)
    records.append(
        _identity(
            system,
            identity_id,
            "matrix",
            fit_type,
            fold,
            klass,
            None,
            None,
            category,
            status,
            residual,
            n_tested,
            {"fold": fold, "class": klass, "map": identity_id},
        )
    )
    if failing:
        _fail_identity(identity_id, fold=fold, klass=klass, residual=residual, tolerance=RECOVERY)
    return status


def _fit_one(run, system_name, ell, jay, weights, voids, prefixes, columns):
    design, target, used = _design(prefixes, columns, ell, jay, weights, voids)
    if design is None:
        run.ledger.add(system_name, "S5", "fit", "SKIPPED_UNAVAILABLE_MAP", 1)
        return None, {"sigma": None, "sigma_1": None, "ratios": None, "n_inverted": 0}, "UNAVAILABLE_EMPTY", 0, 0
    run.note_svd()
    run.ledger.add(system_name, "S5", "fit", "ATTEMPTED", 1, "valid_finite")
    solution, report = fit_from_svd(design, target)
    category = rank_category_from_ratios(report.get("ratios"), report.get("sigma_1"), columns, False)
    return solution, report, category, int(design.shape[0]), columns


def _kappa_norm(matrix: np.ndarray | None, rows: int) -> float | None:
    if matrix is None:
        return None
    if rows == 3:
        return float(np.linalg.norm(matrix[2, :]))
    return 0.0


def stage_s5(run, ctx) -> None:
    run.check_deadline("S5")
    weights = ctx["P_h"]
    for system_name in ("SYS-O6", "SYS-PC", "SYS-FK", "SYS-NC1", "SYS-NC2", "SYS-NC3", "SYS-LIM"):
        run.check_deadline(f"S5 {system_name}")
        system = ctx["systems"][system_name]
        if not system["admissible"]:
            # M-2. Assign the inadmissible skip at this system's S5 point.
            if run.stopped:
                run.ledger.dump_remaining("SKIPPED_PRIOR_STOP", system=system_name, stage="S5")
            else:
                run.ledger.dump_remaining("SKIPPED_SYSTEM_INADMISSIBLE", system=system_name, stage="S5")
            run.write_json(
                f"fit_freeze_{system_name}.json",
                {
                    "system": system_name,
                    "system_inadmissible": True,
                    "fitted_matrices": [],
                    "rank_reports": [],
                    "normal_equation_terms": [],
                    "matrix_identities": [],
                    "cancellation_diagnostics": [],
                    "kappa_row_norms": [],
                    "frozen_before_evaluation": True,
                },
            )
            run.checkpoint(f"S5 {system_name}")
            continue
        ell = system["L"]
        jay = system["J"]
        gee = system["G"]
        arr = system["r"]
        voids = system["voids"]
        maps = {}
        fitted = []
        ranks = []
        terms = []
        identities = []
        kappa_norms = []
        for fold_name, fit_prefixes, _evaluation in folds():
            maps[fold_name] = {}
            cells = [("global", None, list(fit_prefixes))]
            for klass in CLASS_ORDER:
                cells.append(("class", klass, [prefix for prefix in fit_prefixes if ctx["class_of"][prefix] == klass]))
            solved = {}
            for fit_type, klass, prefixes in cells:
                full_sol, full_report, full_cat, full_rows, _cols = _fit_one(
                    run, system_name, ell, jay, weights, voids, prefixes, 3
                )
                mu_sol, mu_report, mu_cat, mu_rows, _mu_cols = _fit_one(
                    run, system_name, ell, jay, weights, voids, prefixes, 2
                )
                key = "global" if fit_type == "global" else klass
                maps[fold_name][key] = {
                    "full": full_sol,
                    "mu": mu_sol,
                    "full_category": full_cat,
                    "mu_category": mu_cat,
                }
                solved[key] = (full_sol, full_cat, mu_sol, mu_cat)
                for map_name, solution, report, category, n_rows, n_cols in (
                    ("full", full_sol, full_report, full_cat, full_rows, 3),
                    ("mu", mu_sol, mu_report, mu_cat, mu_rows, 2),
                ):
                    stored = None if solution is None else np.asarray(solution, dtype=np.float64)
                    packed = None if stored is None else matrix_record(stored)
                    fitted.append(
                        {
                            "system": system_name,
                            "fit_type": fit_type,
                            "fold": fold_name,
                            "class": klass,
                            "map": "B" if map_name == "full" else "A",
                            "values": None if packed is None else packed["values"],
                            "sha256": None if packed is None else packed["sha256"],
                        }
                    )
                    ranks.append(
                        {
                            "system": system_name,
                            "fit_type": fit_type,
                            "fold": fold_name,
                            "class": klass,
                            "map": map_name,
                            "n_rows": n_rows,
                            "n_cols": n_cols,
                            "sigma": report.get("sigma"),
                            "sigma_1": report.get("sigma_1"),
                            "ratios": report.get("ratios"),
                            "rank_category": category,
                            "n_inverted": report.get("n_inverted") or 0,
                            "b3_status": None,
                        }
                    )
                    kappa_norms.append(
                        {
                            "system": system_name,
                            "fit_type": fit_type,
                            "fold": fold_name,
                            "class": klass,
                            "map": map_name,
                            "kappa_row_norm": _kappa_norm(stored, n_cols if map_name == "mu" else 3),
                            "role": "diagnostic",
                        }
                    )
                _matrix_identities(
                    system_name,
                    system,
                    fold_name,
                    fit_type,
                    klass,
                    full_sol,
                    full_cat,
                    mu_sol,
                    mu_cat,
                    identities,
                )
            if system_name in B3_SYSTEMS:
                _b3_fold(run, system_name, system, fold_name, fit_prefixes, voids, jay, ranks, ctx)
            for fit_type, klass, prefixes in cells:
                gram, rhs, _used = _sum_normal(prefixes, gee, arr, voids)
                ident = fold_name if klass is None else f"{fold_name}:{klass}"
                scope = "fold" if klass is None else "foldxclass"
                terms.append(_term(system_name, scope, ident, "sumG", gram))
                terms.append(_term(system_name, scope, ident, "sumr", rhs))
                terms.append(_term(system_name, scope, ident, "sumG_mumu", gram[:2, :2]))
                terms.append(_term(system_name, scope, ident, "sumr_mu", rhs[:2, :]))
        for prefix in range(16):
            if prefix in voids or prefix not in gee:
                continue
            terms.append(_term(system_name, "prefix", str(prefix), "G", gee[prefix]))
            terms.append(_term(system_name, "prefix", str(prefix), "r", arr[prefix]))
        cancellation = _cancellation(system_name, system, ctx)
        system["maps"] = maps
        system["matrix_identities"] = identities
        payload = {
            "system": system_name,
            "system_inadmissible": False,
            "fitted_matrices": fitted,
            "rank_reports": ranks,
            "b3_stacks": [row for row in ranks if row.get("b3_status")],
            "normal_equation_terms": terms,
            "matrix_identities": identities,
            "cancellation_diagnostics": cancellation,
            "kappa_row_norms": kappa_norms,
            "frozen_before_evaluation": True,
        }
        run.write_json(f"fit_freeze_{system_name}.json", payload)
        run.checkpoint(f"S5 {system_name}")
        run.log(f"fit freeze {system_name} written")


def _residual(solution, target) -> float | None:
    if solution is None or target is None:
        return None
    return max_abs(np.asarray(solution, dtype=np.float64) - np.asarray(target, dtype=np.float64))


def _matrix_identities(system_name, system, fold, fit_type, klass, full_sol, full_cat, mu_sol, mu_cat, identities):
    if system_name == "SYS-O6" and fit_type in ("global", "class"):
        target = system["B_true"]
        _apply_check(
            identities,
            system_name,
            f"O6-B-{fit_type}-{fold}-{klass}",
            fit_type,
            fold,
            klass,
            full_cat,
            _residual(full_sol, target),
            stop=True,
        )
        return
    if system_name == "SYS-PC" and fit_type == "global":
        c_mat = system["C"]
        b_target = np.vstack((c_mat[0], c_mat[1], np.zeros(8, dtype=np.float64)))
        a_target = c_mat[:2, :]
        joint = _joint_category(full_cat, mu_cat)
        _apply_check(identities, system_name, f"PC-global-B-{fold}", "global", fold, None, joint, _residual(full_sol, b_target), stop=True)
        _apply_check(identities, system_name, f"PC-global-A-{fold}", "global", fold, None, joint, _residual(mu_sol, a_target), stop=True)
        return
    if system_name == "SYS-PC" and fit_type == "class":
        from ckappa_classfit.classes import CHI

        target = diag3(1.0, 1.0, CHI[klass]) @ system["C"]
        _apply_check(
            identities,
            system_name,
            f"PC-class-B-{fold}-{klass}",
            "class",
            fold,
            klass,
            full_cat,
            _residual(full_sol, target),
            stop=True,
        )
        return
    if system_name == "SYS-FK":
        b_target = system["C_full"]
        a_target = system["C_mu"]
        _apply_check(identities, system_name, f"FK-B-{fit_type}-{fold}-{klass}", fit_type, fold, klass, full_cat, _residual(full_sol, b_target), stop=True)
        _apply_check(identities, system_name, f"FK-A-{fit_type}-{fold}-{klass}", fit_type, fold, klass, mu_cat, _residual(mu_sol, a_target), stop=True)
        return
    if system_name == "SYS-NC2":
        _d5(system, fold, fit_type, klass, full_sol, full_cat, identities)
        return
    if system_name == "SYS-LIM" and fit_type == "global":
        _d6(system, fold, full_sol, full_cat, mu_sol, mu_cat, identities)
        return
    if system_name == "SYS-LIM" and fit_type == "class" and fold in D7_FOLDS:
        target = diag3(1.0, 1.0, -1.0) @ system["C"]
        _apply_check(
            identities,
            system_name,
            f"D7-{fold}-{klass}",
            "class",
            fold,
            klass,
            full_cat,
            _residual(full_sol, target),
            stop=False,
            investigate=True,
        )


_D6_VERDICTS = ("PASS", "FAIL", "INVESTIGATE")


def _d5(system, fold, fit_type, klass, full_sol, full_cat, identities) -> None:
    """Descriptive D5 for SYS-NC2 (v1.3 C4.4, premise table).

    Dg2 is constant, so the full model is exact when the design has resolved
    full column rank. The record is reported. It does not stop and it does
    not enter VALIDATION.
    """
    slope = system.get("slope") or {}
    target = next(iter(slope.values())) if slope else None
    residual = _residual(full_sol, target)
    if full_cat == "UNAVAILABLE_EMPTY":
        status = "UNAVAILABLE"
        n_tested = 0
    elif full_cat == "UNRESOLVED":
        status = "REFERENCE_RANK_UNRESOLVED"
        n_tested = 0
    elif full_cat in ("LOWER", "ZERO_NONEMPTY"):
        status = "NOT_APPLICABLE_RANK"
        n_tested = 0
    elif full_cat != "FULL" or residual is None:
        status = "NOT_EVALUATED"
        n_tested = 0
    else:
        status = "REPORTED"
        n_tested = 1
    record = _identity(
        "SYS-NC2",
        f"D5-{fit_type}-{fold}-{klass}",
        "descriptive",
        fit_type,
        fold,
        klass,
        None,
        None,
        full_cat,
        status,
        residual,
        n_tested,
        {"fold": fold, "class": klass, "map": "D5"},
    )
    record["tolerance_abs"] = None
    record["tolerance_rel"] = None
    record["role"] = "descriptive"
    record["expectation"] = (
        "Dg2 is constant, so the full model is exact when the design has resolved full column rank. "
        "Gain = L_mu >= 0 under that premise. Reported. Not evidence of a covariance register."
    )
    identities.append(record)


def _d6_premise_status(category: str, residual: float | None) -> str:
    """RL-3. Premise status only. No pass, fail, or investigate verdict."""
    if category == "UNAVAILABLE_EMPTY":
        return "UNAVAILABLE"
    if category == "UNRESOLVED":
        return "REFERENCE_RANK_UNRESOLVED"
    if category in ("LOWER", "ZERO_NONEMPTY"):
        return "NOT_APPLICABLE_RANK"
    if category != "FULL" or residual is None:
        return "NOT_EVALUATED"
    return "REPORTED"


def _reject_d6_verdict(value, where: str) -> None:
    if isinstance(value, str):
        if value in _D6_VERDICTS:
            integrity_stop("D6 record carries a verdict", where=where, value=value)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key in _D6_VERDICTS:
                integrity_stop("D6 record carries a verdict key", where=where, key=key)
            _reject_d6_verdict(item, f"{where}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_d6_verdict(item, f"{where}[{index}]")


def _d6(system, fold, full_sol, full_cat, mu_sol, mu_cat, identities):
    fit_orbits = None
    for name, fit_names, _evaluation in FOLD_SPEC:
        if name == fold:
            fit_orbits = fit_names
            break
    joint = _joint_category(full_cat, mu_cat)
    residual = None
    if fit_orbits is not None:
        lam = _lambda(system, fit_orbits)
        if lam is not None:
            c_mat = system["C"]
            b_target = np.vstack((c_mat[0], c_mat[1], lam * c_mat[2]))
            a_target = c_mat[:2, :]
            parts = [value for value in (_residual(full_sol, b_target), _residual(mu_sol, a_target)) if value is not None]
            residual = None if not parts else max(parts)
    status = _d6_premise_status(joint, residual)
    record = _identity(
        "SYS-LIM",
        f"D6-{fold}",
        "matrix",
        "global",
        fold,
        None,
        None,
        None,
        joint,
        status,
        residual,
        1 if residual is not None else 0,
        {"fold": fold},
    )
    # Residual and premise status only. A tolerance would be a verdict threshold.
    record["tolerance_abs"] = None
    record["tolerance_rel"] = None
    _reject_d6_verdict(record, f"D6-{fold}")
    identities.append(record)


def _lambda(system, fit_orbits):
    numerator = 0.0
    denominator = 0.0
    for orbit in fit_orbits:
        sign = system["orbit_sign"][orbit]
        mass = 0.0
        for prefix in ORBITS[orbit]:
            if prefix not in system["G"]:
                continue
            mass += float(system["G"][prefix][2, 2])
        numerator += float(sign) * mass
        denominator += mass
    if denominator == 0.0:
        return None
    return numerator / denominator


def _b3_fold(run, system_name, system, fold, fit_prefixes, voids, jay, ranks, ctx):
    blocks = [("global", None, list(fit_prefixes))]
    for klass in CLASS_ORDER:
        blocks.append(("class", klass, [prefix for prefix in fit_prefixes if ctx["class_of"][prefix] == klass]))
    for fit_type, klass, prefixes in blocks:
        usable = [prefix for prefix in prefixes if prefix not in voids]
        if not usable:
            run.ledger.add(system_name, "S5", "b3_stack", "SKIPPED_UNAVAILABLE_MAP", 1)
            ranks.append(
                {
                    "system": system_name,
                    "fit_type": fit_type,
                    "fold": fold,
                    "class": klass,
                    "map": "b3_stack",
                    "n_rows": 0,
                    "n_cols": 8,
                    "sigma": None,
                    "sigma_1": None,
                    "ratios": None,
                    "rank_category": "UNAVAILABLE_EMPTY",
                    "n_inverted": 0,
                    "b3_status": "NOT_FORMED",
                }
            )
            continue
        rows = []
        for prefix in usable:
            for continuation in range(16):
                rows.append(jay[(prefix, continuation)])
        stack = np.vstack(rows)
        run.note_svd()
        run.ledger.add(system_name, "S5", "b3_stack", "ATTEMPTED", 1, "valid_finite")
        sigma = np.linalg.svd(stack, full_matrices=False, compute_uv=False)
        sigma_list = [float(value) for value in sigma]
        status = b3_status(sigma_list, True)
        sigma1 = sigma_list[0] if sigma_list else 0.0
        ratios = None if sigma1 == 0.0 else [value / sigma1 for value in sigma_list]
        ranks.append(
            {
                "system": system_name,
                "fit_type": fit_type,
                "fold": fold,
                "class": klass,
                "map": "b3_stack",
                "n_rows": int(stack.shape[0]),
                "n_cols": 8,
                "sigma": sigma_list,
                "sigma_1": sigma1,
                "ratios": ratios,
                "rank_category": rank_category_from_ratios(ratios, sigma1, 8, False),
                "n_inverted": 0,
                "b3_status": status,
            }
        )
        if status == "RESOLVED_THIRD_DIRECTION":
            integrity_stop(
                "resolved extended-B3 third direction",
                system=system_name,
                fold=fold,
                klass=klass,
                fit_type=fit_type,
                third_ratio=None if ratios is None or len(ratios) < 3 else ratios[2],
                also="PIPELINE INVALID",
            )


def _cancellation(system_name, system, ctx) -> list:
    rows = []
    gee = system["G"]
    for orbit, members in ORBITS.items():
        pieces = []
        labels = (("G_kappa_mux", 2, 0), ("G_kappa_muy", 2, 1), ("G_mux_muy", 0, 1))
        sums = {name: 0.0 for name, _i, _j in labels}
        scales = {name: 0.0 for name, _i, _j in labels}
        for prefix in members:
            if prefix not in gee:
                continue
            for name, i, j in labels:
                value = float(gee[prefix][i, j])
                sums[name] += value
                scales[name] += abs(value)
        for name, _i, _j in labels:
            tolerance = cancellation_tolerance([scales[name]])
            residual = abs(sums[name])
            rows.append(
                {
                    "system": system_name,
                    "orbit": orbit,
                    "name": name,
                    "value": sums[name],
                    "tolerance": tolerance,
                    "scale": scales[name],
                    "pass": residual <= tolerance,
                    "role": "diagnostic",
                }
            )
        if system_name in ("SYS-NC1", "SYS-NC2", "SYS-NC3"):
            vector = np.zeros(2, dtype=np.float64)
            for prefix in members:
                if prefix not in gee:
                    continue
                mu_x = float(ctx["theta"][prefix, 0])
                mu_y = float(ctx["theta"][prefix, 1])
                if system_name == "SYS-NC1":
                    from ckappa_oracle.geometry import g_gradient

                    gradient = g_gradient(ctx["nc1_coef"], mu_x, mu_y)
                elif system_name == "SYS-NC2":
                    gradient = np.array([ctx["c2"], 0.0], dtype=np.float64)
                else:
                    gradient = np.array([3.0 * ctx["c3"] * mu_x * mu_x, 0.0], dtype=np.float64)
                vector += float(gee[prefix][2, 2]) * np.asarray(gradient, dtype=np.float64)
            packed = matrix_record(vector.reshape(1, 2))
            rows.append(
                {
                    "system": system_name,
                    "orbit": orbit,
                    "name": "sum_G_kk_Dg",
                    "value": packed["values"],
                    "sha256": packed["sha256"],
                    "tolerance": None,
                    "scale": None,
                    "role": "diagnostic",
                }
            )
    return rows
