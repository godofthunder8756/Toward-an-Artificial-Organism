"""Hand-made fixture checks. Does not load drawn arrays and does not run stages S0–S8."""

from __future__ import annotations

from fractions import Fraction

from ckappa_classfit.accounting import Ledger
from ckappa_classfit.classes import CHI, DECLARED_CLASS_PREFIXES, declared_matches_xor, class_of_prefix
from ckappa_classfit.aggregate import pool_records
from ckappa_classfit.evaluate import _crosses_lim, _crosses_pc
from ckappa_classfit.pinned import DECLARED_N_O1, EXACT_T, FROZEN_RUNTIME, SCHEDULED_FLOAT
from ckappa_classfit.rankcats import b3_status, rank_category_from_ratios, skip_reason
from ckappa_classfit.report import E37_10, E37_3, E37_4, E38_15, FK_SENTENCE, L194, L202, TEMPLATE, render
from ckappa_classfit.schedule import (
    B3_STACKS,
    EDITS_ALL,
    EXACT_O1,
    FLOAT_MAX,
    LOSS_RECORDS,
    POOLED,
    SVDS,
)


def _eq(left, right, label: str) -> None:
    if left != right:
        raise SystemExit(f"{label}: {left!r} != {right!r}")


def check_schedule() -> None:
    _eq(FLOAT_MAX, 3443968, "SCHEDULED_FLOAT")
    _eq(SCHEDULED_FLOAT, 3443968, "pinned float")
    _eq(EXACT_O1, 272, "O1")
    _eq(DECLARED_N_O1, 272, "pinned O1")
    _eq(SVDS, 541, "SVDs")
    _eq(LOSS_RECORDS, 16128, "loss records")
    _eq(EDITS_ALL, 688128, "edits")
    _eq(B3_STACKS, 120, "B3")
    _eq(POOLED, 336, "pooled")
    _eq(int(FROZEN_RUNTIME["scheduled_float_propagations"]), 788480, "inherited schedule")
    _eq(int(FROZEN_RUNTIME["classfit_scheduled_float_propagations"]), 3443968, "classfit schedule")


def check_ranks() -> None:
    _eq(rank_category_from_ratios(None, None, 3, True), "UNAVAILABLE_EMPTY", "empty")
    _eq(rank_category_from_ratios([1.0], 0.0, 3, False), "ZERO_NONEMPTY", "zero")
    _eq(rank_category_from_ratios([1.0, 1e-8, 1e-12], 1.0, 3, False), "UNRESOLVED", "band")
    _eq(rank_category_from_ratios([1.0, 1e-4, 1e-12], 1.0, 3, False), "LOWER", "lower")
    _eq(rank_category_from_ratios([1.0, 0.5, 0.1], 2.0, 3, False), "FULL", "full")
    _eq(b3_status(None, False), "NOT_FORMED", "b3 absent")
    _eq(b3_status([0.0, 0.0, 0.0], True), "ZERO", "b3 zero")
    from ckappa_oracle.io import PackageStop

    try:
        short = b3_status([1.0, 0.2], True)
    except PackageStop as exc:
        _eq(exc.kind, "INTEGRITY STOP", "b3 short kind")
        _eq(exc.exit_code, 7, "b3 short exit")
        _eq(exc.detail.get("diagnosis"), "PIPELINE INVALID (B3 short stack)", "b3 short diagnosis")
    else:
        raise SystemExit(f"b3 short stack returned {short!r}")
    _eq(b3_status([1.0, 0.2, 1e-8], True), "UNRESOLVED-B3", "b3 band")
    _eq(b3_status([1.0, 0.2, 1e-5], True), "RESOLVED_THIRD_DIRECTION", "b3 third")
    _eq(b3_status([1.0, 0.2, 1e-12], True), "PASS", "b3 pass")


def check_skip() -> None:
    _eq(
        skip_reason(stopped=True, system_inadmissible=True, prefix_void=True, map_unavailable=True),
        "SKIPPED_PRIOR_STOP",
        "stop",
    )
    _eq(
        skip_reason(stopped=False, system_inadmissible=True, prefix_void=True, map_unavailable=True),
        "SKIPPED_SYSTEM_INADMISSIBLE",
        "system",
    )
    _eq(
        skip_reason(stopped=False, system_inadmissible=False, prefix_void=True, map_unavailable=True),
        "SKIPPED_PREFIX_VOID",
        "void",
    )
    _eq(
        skip_reason(stopped=False, system_inadmissible=False, prefix_void=False, map_unavailable=True),
        "SKIPPED_UNAVAILABLE_MAP",
        "map",
    )
    _eq(
        skip_reason(stopped=False, system_inadmissible=False, prefix_void=False, map_unavailable=False),
        None,
        "attempt",
    )


def check_classes() -> None:
    if not declared_matches_xor():
        raise SystemExit("XOR table does not match the declared prefixes")
    classes = class_of_prefix()
    for klass, row in DECLARED_CLASS_PREFIXES.items():
        for prefix in row.values():
            _eq(classes[prefix], klass, "class")
    _eq(CHI["I"], 1.0, "chi I")
    _eq(CHI["X"], -1.0, "chi X")
    _eq(CHI["Y"], -1.0, "chi Y")
    _eq(CHI["XY"], 1.0, "chi XY")
    _eq(5 | (5 << 4), 85, "X mask")
    _eq(10 | (10 << 4), 170, "Y mask")


def check_crossing() -> None:
    import numpy as np

    psi = np.array([0.4, -0.2, 0.1])
    same = np.array([0.5, -0.3, 0.0])
    flipped = np.array([-0.1, -0.2, 0.0])
    if _crosses_pc(psi, same):
        raise SystemExit("same-sign edit was marked as a crossing")
    if not _crosses_pc(psi, flipped):
        raise SystemExit("sign change was not marked as a crossing")
    if _crosses_lim(np.array([0.8, 0.0, 0.0]), np.array([0.7, 0.0, 0.0]), 0.4):
        raise SystemExit("same side of t was marked as a crossing")
    if not _crosses_lim(np.array([0.8, 0.0, 0.0]), np.array([0.2, 0.0, 0.0]), 0.4):
        raise SystemExit("threshold crossing was missed")


def check_c2_arithmetic() -> None:
    weights = [Fraction(1, 16) for _ in range(16)]
    total = sum(weights, start=Fraction(0))
    _eq(total, Fraction(1), "toy P_sum")
    p_sum = float(total)
    acc = 0.0
    for weight in weights:
        acc += float(weight) * 4.0
    rho = acc ** 0.5
    c2 = rho / (p_sum ** 0.5)
    _eq(c2, 2.0, "toy c2")
    _eq(EXACT_T, "6299716077234553896/15613266622202707711", "exact t")


def check_ledger() -> None:
    ledger = Ledger()
    ledger.add("SYS-O6", "S6", "propagation", "ATTEMPTED", 1, "valid_finite")
    ledger.dump_remaining("SKIPPED_PRIOR_STOP")
    if not ledger.close_all():
        raise SystemExit("ledger did not close")
    matched = [row for row in ledger.records() if row["system"] == "SYS-O6" and row["stage"] == "S6" and row["unit"] == "propagation"]
    _eq(matched[0]["counts"]["ATTEMPTED"], 1, "attempted")
    _eq(matched[0]["remaining"], 0, "remaining")


def check_pool() -> None:
    rows = pool_records("SYS-NC1", {"admissible": False, "voids": [0]}, [], False)
    _eq(len(rows), 48, "one system pool")
    _eq(rows[0]["formed"], False, "unformed")
    _eq(rows[0]["not_formed_reason"], "RESTRICTED COMPARATOR NOT ADMISSIBLE", "reason")


def check_report() -> None:
    text = TEMPLATE + render({"stop_kind": "PREFLIGHT FAILED", "labels": [], "VALIDATION": {}, "HEADROOM": {}})
    lowered = text.lower()
    for banned in ("floor", "phase", "seal"):
        if banned in lowered:
            raise SystemExit(f"report template contains {banned}")
    for required in (
        E37_3,
        E37_4,
        E37_10,
        E38_15,
        L202,
        L194,
        FK_SENTENCE,
        "Comparator squared prediction error divided by actual response energy.",
        "Oracle-scale headroom only.",
        "incomplete",
        "D6 cells report the residual and the premise status only. They do not carry PASS or FAIL. INVESTIGATE belongs to D7 only.",
        "The reverse guard direction is recorded on its own and does not stop.",
    ):
        if required not in text:
            raise SystemExit("report template is missing a required sentence")


def check_manifest() -> None:
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "classfit_manifest.json"
    if not path.is_file():
        raise SystemExit("classfit_manifest.json is absent")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("sealed") is not False:
        raise SystemExit("manifest sealed is not false")
    if manifest.get("frozen_runtime") != FROZEN_RUNTIME:
        raise SystemExit("manifest frozen_runtime does not match pinned constants")
    application = manifest.get("standing_approval_application") or {}
    if application.get("status") != "PENDING" or application.get("sha256") is not None:
        raise SystemExit("application is not pending")
    if "phase" in manifest:
        raise SystemExit("manifest contains a phase key")


def _walk_verdicts(value, found: list) -> None:
    if isinstance(value, str) and value in ("PASS", "FAIL", "INVESTIGATE"):
        found.append(value)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key in ("PASS", "FAIL", "INVESTIGATE"):
                found.append(key)
            _walk_verdicts(item, found)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _walk_verdicts(item, found)


def check_rho_domain() -> None:
    import inspect

    import numpy as np
    from ckappa_oracle.io import PackageStop
    from ckappa_classfit.construction import rho_nc1_exact_law

    params = inspect.signature(rho_nc1_exact_law).parameters
    for banned in ("voids", "void", "admissible", "admissibility", "run", "ledger"):
        if banned in params:
            raise SystemExit(f"rho_NC1 accepts {banned}")
    coef = np.zeros(6, dtype=np.float64)
    coef[1] = 2.0
    mu_y = [0.0] * 16
    mu_x = [0.0] * 16
    mu_x[0] = 1.0
    weights = [Fraction(0) for _ in range(16)]
    weights[0] = Fraction(1)
    row = rho_nc1_exact_law(coef, mu_x, mu_y, weights)
    _eq(row["n_prefixes"], 16, "rho prefixes")
    _eq(row["prefix_domain"], "exact-law a=0..15", "rho domain")
    _eq(row["independent_of_sys_nc1_voids"], True, "rho voids")
    _eq(row["independent_of_sys_nc1_admissibility"], True, "rho admissibility")
    _eq(row["e39_7_skip_applied"], False, "rho skip")
    _eq(row["unit"], "coefficient_rule", "rho unit")
    _eq(row["summation_order"], "sequential a=0..15", "rho order")
    _eq(row["rho_NC1"], 2.0, "rho prefix 0")
    _eq(row["M4"], 1.0, "m4 prefix 0")
    _eq(row["c2"], 2.0, "c2")
    _eq(row["c3"], 2.0 / 3.0, "c3")
    mu_x[0] = 0.0
    mu_x[15] = 1.0
    weights[0] = Fraction(0)
    weights[15] = Fraction(1)
    last = rho_nc1_exact_law(coef, mu_x, mu_y, weights)
    _eq(last["rho_NC1"], 2.0, "rho prefix 15")
    _eq(last["M4"], 1.0, "m4 prefix 15")
    try:
        rho_nc1_exact_law(coef, [0.0], [0.0], [Fraction(1)])
    except PackageStop as exc:
        _eq(exc.kind, "INTEGRITY STOP", "short rho")
    else:
        raise SystemExit("a short prefix list was accepted")


def check_reverse_guard() -> None:
    import numpy as np
    from ckappa_oracle.io import PackageStop
    from ckappa_classfit.evaluate import _Cell, _guard_and_maybe_stop

    key = ("global_full", "global", "AB->CD", None, "0.1")
    guards = {key: _Cell()}
    beliefs = {
        "actual": np.array([0.125, 0.5]),
        "global_full": np.array([0.25, 0.5]),
    }
    thetas = {
        "actual": np.array([1.0, 0.0, 0.0]),
        "global_full": np.array([1.5, 0.0, 0.0]),
    }
    forecasts = {
        "actual": np.array([0.0, 0.0, 0.0]),
        "global_full": np.array([0.0, 0.0, 0.25]),
    }
    _guard_and_maybe_stop(
        guards, key, False, True, beliefs, thetas, forecasts, "global_full", 3, 4, 5, 1.0, "0.1", "FULL"
    )
    cell = guards[key]
    _eq(cell.n_reverse, 1, "reverse count")
    _eq(cell.n_stop, 0, "reverse does not count as a stop")
    _eq(cell.first, None, "reverse leaves first_mismatch empty")
    reverse = cell.first_reverse
    if not isinstance(reverse, dict):
        raise SystemExit("reverse record is missing")
    _eq(reverse["min_p_actual"], 0.125, "reverse min p actual")
    _eq(reverse["min_p_predicted"], 0.25, "reverse min p predicted")
    _eq(reverse["chart_diff_max_abs"], 0.5, "reverse chart")
    _eq(reverse["recovery_residual_max_abs"], 0.25, "reverse residual")
    _eq(reverse["edit"]["prefix"], 3, "reverse edit")
    _guard_and_maybe_stop(
        guards, key, False, True, beliefs, thetas, forecasts, "global_full", 9, 1, 2, -1.0, "0.1", "FULL"
    )
    _eq(cell.n_reverse, 2, "later reverse is counted")
    _eq(cell.first_reverse["edit"]["prefix"], 3, "first reverse record is kept")
    try:
        _guard_and_maybe_stop(
            guards, key, True, False, beliefs, thetas, forecasts, "global_full", 1, 2, 3, 1.0, "0.1", "FULL"
        )
    except PackageStop as exc:
        _eq(exc.kind, "PIPELINE INVALID", "forward guard stops")
    else:
        raise SystemExit("actual-valid guard mismatch did not stop")
    _eq(cell.n_stop, 1, "forward count")
    if cell.first is None or cell.first["edit"]["prefix"] != 1:
        raise SystemExit("first_mismatch was not recorded separately")
    _eq(cell.first_reverse["edit"]["prefix"], 3, "forward stop does not replace the reverse record")


def check_d6_premise() -> None:
    import numpy as np
    from ckappa_classfit.fits import _d6, _d6_premise_status, _status_for

    gee = {}
    for prefix in range(16):
        matrix = np.zeros((3, 3), dtype=np.float64)
        matrix[2, 2] = 1.0
        gee[prefix] = matrix
    c_mat = np.ones((3, 8), dtype=np.float64)
    system = {
        "C": c_mat,
        "orbit_sign": {"A": 1, "B": -1, "C": -1, "D": -1},
        "G": gee,
    }
    matched = np.vstack((c_mat[0], c_mat[1], np.zeros(8, dtype=np.float64)))
    mu = c_mat[:2, :]
    identities = []
    _d6(system, "AB->CD", matched, "FULL", mu, "FULL", identities)
    _d6(system, "AB->CD", np.zeros((3, 8)), "FULL", mu, "FULL", identities)
    _d6(system, "AB->CD", matched, "LOWER", mu, "FULL", identities)
    _eq(len(identities), 3, "d6 rows")
    reported, large, lower = identities
    _eq(reported["status"], "REPORTED", "d6 reported")
    _eq(reported["premise_rank_category"], "FULL", "d6 premise")
    _eq(reported["max_abs_residual"], 0.0, "d6 zero residual")
    _eq(reported["tolerance_abs"], None, "d6 tolerance")
    if not (large["max_abs_residual"] is not None and large["max_abs_residual"] > 1e-9):
        raise SystemExit("large D6 residual was not stored")
    _eq(large["status"], "REPORTED", "large d6 is not a failure")
    _eq(lower["status"], "NOT_APPLICABLE_RANK", "d6 lower premise")
    _eq(_d6_premise_status("UNRESOLVED", 0.0), "REFERENCE_RANK_UNRESOLVED", "d6 unresolved")
    _eq(_d6_premise_status("UNAVAILABLE_EMPTY", None), "UNAVAILABLE", "d6 empty")
    for row in identities:
        found = []
        _walk_verdicts(row, found)
        if found:
            raise SystemExit(f"D6 record contains {found}")
    status, tested, failing = _status_for("FULL", 1.0, stop=False, investigate=True)
    _eq(status, "INVESTIGATE", "d7 investigate")
    _eq(tested, 1, "d7 tested")
    _eq(failing, False, "d7 does not stop")


def check_memory_budget() -> None:
    import inspect

    from ckappa_classfit.pinned import (
        ADDED_MEMORY_RECORDS,
        ADDED_RECORD_BYTES,
        ADDED_SERIALIZATION_BYTES,
        ANNEX_V2_INCREMENTAL_BYTES,
        FITTED_MATRIX_RECORDS,
        INCREMENTAL_BYTES,
        LABEL_RECORDS,
        NORMAL_EQUATION_RECORDS,
        PACKAGE_BUDGET_BYTES,
    )
    from ckappa_classfit.preflight import address_space_exceeds
    from ckappa_classfit.runstate import OUTPUT_DIR

    _eq(FITTED_MATRIX_RECORDS, 420, "fitted matrices")
    _eq(NORMAL_EQUATION_RECORDS, 1064, "normal equations")
    _eq(LABEL_RECORDS, 30, "labels")
    _eq(ADDED_MEMORY_RECORDS, 1514, "added records")
    _eq(ADDED_RECORD_BYTES, 1514 * 2048, "added record bytes")
    _eq(ADDED_SERIALIZATION_BYTES, 1514 * 4096, "added serialization")
    _eq(INCREMENTAL_BYTES, ANNEX_V2_INCREMENTAL_BYTES + ADDED_RECORD_BYTES + ADDED_SERIALIZATION_BYTES, "incremental")
    _eq(PACKAGE_BUDGET_BYTES, INCREMENTAL_BYTES * 2, "budget factor")
    _eq(PACKAGE_BUDGET_BYTES, 316_737_056, "package budget")
    cap = 4_000_000_000
    _eq(address_space_exceeds(1_000_000, PACKAGE_BUDGET_BYTES, cap), False, "vmpeak under cap")
    _eq(address_space_exceeds(cap - PACKAGE_BUDGET_BYTES + 1, PACKAGE_BUDGET_BYTES, cap), True, "vmpeak over cap")
    if "rss" in inspect.signature(address_space_exceeds).parameters:
        raise SystemExit("the RLIMIT comparison accepts RSS")
    _eq(OUTPUT_DIR, "classfit_outputs", "output directory name")


def check_outputs_gate() -> None:
    import tempfile
    from pathlib import Path

    from ckappa_oracle.io import PackageStop
    from ckappa_classfit.preflight import OUTPUT_DIR_NAME, check_outputs_directory, outputs_directory_state

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _eq(outputs_directory_state(root), "absent", "outputs absent")
        _eq(check_outputs_directory(root), "absent", "absent is allowed")
        (root / OUTPUT_DIR_NAME).mkdir()
        _eq(outputs_directory_state(root), "empty", "outputs empty")
        _eq(check_outputs_directory(root), "empty", "empty is allowed")
        (root / OUTPUT_DIR_NAME / "stage_S0_preflight.json").write_text("{}\n", encoding="utf-8")
        _eq(outputs_directory_state(root), "nonempty", "outputs nonempty")
        try:
            check_outputs_directory(root)
        except PackageStop as exc:
            _eq(exc.kind, "INTEGRITY STOP", "nonempty outputs")
        else:
            raise SystemExit("a nonempty classfit_outputs directory was accepted")


def check_oracle_rehash() -> None:
    from pathlib import Path

    from ckappa_classfit.pinned import (
        ORACLE_SEALED_MANIFEST_SHA256,
        ORACLE_SEALED_OUTPUT_SHA256,
        oracle_rehash_row,
    )

    matched = oracle_rehash_row("abc", "abc")
    _eq(matched["match"], True, "rehash match")
    _eq(matched["stops"], False, "rehash match does not stop")
    missing = oracle_rehash_row(None, ORACLE_SEALED_MANIFEST_SHA256)
    _eq(missing["match"], False, "rehash miss")
    _eq(missing["stops"], False, "rehash miss does not stop")
    _eq(
        ORACLE_SEALED_MANIFEST_SHA256,
        "4179b71a0110903472d6506686b2f7e0ab2188d9050c9c3f40c31a2fb6b46831",
        "sealed manifest",
    )
    _eq(len(ORACLE_SEALED_OUTPUT_SHA256), 15, "sealed output count")
    _eq(
        ORACLE_SEALED_OUTPUT_SHA256["outputs/stage_O7.json"],
        "994dda0a1e9f4194726abab2420033c8ae266c8802bcf962f7a38ce7c2350116",
        "sealed stage O7",
    )
    text = (Path(__file__).resolve().parents[1] / "run_classfit_package.sh").read_text(encoding="utf-8")
    if "oracle_artifact_rehash" not in text or "oracle_rehash_stops" not in text:
        raise SystemExit("wrapper does not record the oracle rehash")
    if "oracle_rehash_stops = True" in text:
        raise SystemExit("wrapper stops on the oracle rehash")


def main() -> int:
    check_schedule()
    check_ranks()
    check_skip()
    check_classes()
    check_crossing()
    check_c2_arithmetic()
    check_ledger()
    check_pool()
    check_report()
    check_manifest()
    check_rho_domain()
    check_reverse_guard()
    check_d6_premise()
    check_memory_budget()
    check_outputs_gate()
    check_oracle_rehash()
    print("static checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
