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
    _eq(b3_status([0.0, 0.0], True), "ZERO", "b3 zero")
    _eq(b3_status([1.0, 0.2], True), "PASS", "b3 short")
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
    for required in (E37_3, E37_4, E37_10, E38_15, L202, L194, FK_SENTENCE, "Comparator squared prediction error divided by actual response energy.", "Oracle-scale headroom only.", "incomplete"):
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
    print("static checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
