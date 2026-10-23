"""Stages S1 and S2. Inherited O1 and O2 order, written under classfit_outputs."""

from __future__ import annotations

import time
from fractions import Fraction

import numpy as np

from ckappa_oracle import world
from ckappa_oracle.io import PackageStop, integrity_stop
from ckappa_oracle.pinned import fnum
from ckappa_classfit.classes import FOLD_SPEC, ORBITS, folds
from ckappa_classfit.pinned import DECLARED_N_O1

GUARD_FD = fnum("fd_step")
O2_TOL = fnum("o2_tolerance")


def _fail(reason: str, **detail):
    payload = {"reason": reason}
    payload.update(detail)
    raise PackageStop("PIPELINE INVALID", 2, payload)


def _accept_exact(got, expected, truncation: str) -> bool:
    if got == expected:
        return True
    return world.decimal_truncation_50(got) == truncation


def stage_s1(run, stored: dict) -> dict:
    run.check_deadline("S1")
    started = time.perf_counter()
    matrix = world.fraction_transition()
    beliefs = []
    prefix_probability = []
    for prefix in range(16):
        belief, probability = world.filter_prefix(prefix, 4, matrix)
        run.bump_exact(1)
        run.ledger.add("SYS-O6", "S1", "propagation", "ATTEMPTED", 1, "valid_finite")
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
            run.ledger.add("SYS-O6", "S1", "propagation", "ATTEMPTED", 1, "valid_finite")
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
    p_a_exact = []
    for prefix in range(16):
        mass = sum((history_probability[prefix + 16 * continuation] for continuation in range(16)), start=Fraction(0))
        p_a_exact.append(mass)
        if mass != prefix_probability[prefix]:
            failures.append({"check": "prefix probability", "prefix": prefix})
            break
    p_sum_exact = sum(p_a_exact, start=Fraction(0))
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
    if run.exact_count != DECLARED_N_O1:
        failures.append({"check": "exact propagation count", "n_O1": run.exact_count, "declared": DECLARED_N_O1})
    run.t_o1 = time.perf_counter() - started
    run.n_o1 = run.exact_count
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
    charts_exact = []
    for prefix, belief in enumerate(beliefs):
        chart, _marginals = world.chart_from_belief(belief)
        charts_exact.append(chart)
        theta_exact.append([world.fraction_text(value) for value in chart])
        theta[prefix, :] = [float(value) for value in chart]
    p_h = {}
    p_h_exact = {}
    p_a = np.zeros(16, dtype=np.float64)
    for prefix in range(16):
        for continuation in range(16):
            history = prefix + 16 * continuation
            probability = float(history_probability[history])
            p_h[(prefix, continuation)] = probability
            p_h_exact[(prefix, continuation)] = history_probability[history]
            p_a[prefix] += probability
    payload = {
        "stage": "S1",
        "status": "FAIL" if failures else "PASS",
        "n_O1": run.exact_count,
        "T_O1_s": run.t_o1,
        "T_O1_s_source": "perf_counter around stage S1",
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
        "P_sum_exact": world.fraction_text(p_sum_exact),
        "P_a_exact": [world.fraction_text(value) for value in p_a_exact],
        "split_table": split_table,
        "val_readout_rejection": "UNVERIFIED",
        "continuation_strings_shared": True,
        "memory": run.memory_observation(),
    }
    run.write_json("stage_S1_O1.json", payload)
    run.checkpoint("S1")
    run.log("stage S1 written")
    if failures:
        _fail("O1 fixture", failures=failures, mismatch_count=len(mismatches))
    return {
        "theta": theta,
        "charts_exact": charts_exact,
        "beliefs_exact": beliefs,
        "P_h": p_h,
        "P_h_exact": p_h_exact,
        "P_a": p_a,
        "P_a_exact": p_a_exact,
        "P_sum_exact": p_sum_exact,
        "forecasts_exact": forecasts,
        "L_true": {},
    }


def stage_s2(run, ctx: dict) -> None:
    run.check_deadline("S2")
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
                plus[coordinate] += GUARD_FD
                minus[coordinate] -= GUARD_FD
                for sign, point in ((1, plus), (-1, minus)):
                    key = ("S2", prefix, continuation, coordinate, sign)
                    try:
                        forecast, _belief = run.phi(point, continuation, "S2", key)
                    except ValueError as exc:
                        run.ledger.add("SYS-O6", "S2", "propagation", "ATTEMPTED", 1, "value_error")
                        _fail("finite-difference derivative", prefix=prefix, continuation=continuation, error=str(exc))
                    if sign == 1:
                        q_plus = forecast
                    else:
                        q_minus = forecast
                    run.ledger.add("SYS-O6", "S2", "propagation", "ATTEMPTED", 1, "valid_finite")
                finite[:, coordinate] = (q_plus - q_minus) / (2.0 * GUARD_FD)
            difference = float(np.max(np.abs(closed - finite)))
            n_entries += 9
            if difference >= max_abs:
                max_abs = difference
                worst = {"prefix": prefix, "continuation": continuation, "max_abs": difference}
            ctx["L_true"][(prefix, continuation)] = closed
    status = "PASS" if max_abs <= O2_TOL else "FAIL"
    payload = {
        "stage": "S2",
        "status": status,
        "max_abs_difference": max_abs,
        "tolerance": O2_TOL,
        "fd_step": GUARD_FD,
        "entries": n_entries,
        "float_propagations": run.float_count,
        "worst": worst,
        "memory": run.memory_observation(),
    }
    run.write_json("stage_S2_O2.json", payload)
    run.checkpoint("S2")
    run.log("stage S2 written")
    if status == "FAIL":
        _fail("O2 fixture", max_abs_difference=max_abs, tolerance=O2_TOL)
    if run.ledger.counts[("SYS-O6", "S2", "propagation")]["ATTEMPTED"] != 16 * 16 * 3 * 2:
        integrity_stop("O2 propagation count", count=run.ledger.counts[("SYS-O6", "S2", "propagation")]["ATTEMPTED"])
