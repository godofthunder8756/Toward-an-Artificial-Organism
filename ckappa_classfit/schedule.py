"""Scheduled maxima. Each integer is a product of factors named in v1.3 C8.3.

Nothing here is measured. Optional single-prefix fits are absent (E39-6).
"""

from __future__ import annotations

from ckappa_oracle.io import integrity_stop
from ckappa_classfit.pinned import B3_SYSTEMS, DECLARED_N_O1, SCHEDULED_FLOAT, SYSTEM_ORDER

FOLDS = 6
CLASSES = 4
EVAL_PREFIXES_PER_FOLD = 8
CONTINUATIONS = 16
SIGNED_DIRECTIONS = 32
SIZES = 4
PREDICTORS_PER_EDIT = 5
PREFIXES = 16
ORBITS = 4
GROUPS = 3
FIT_TYPES = 2
MODES = 2
N_SYSTEMS = 7

EDITS_PER_FOLD_SIZE = EVAL_PREFIXES_PER_FOLD * CONTINUATIONS * SIGNED_DIRECTIONS
EDITS_PER_FOLD_CLASS_SIZE = 2 * CONTINUATIONS * SIGNED_DIRECTIONS
EDITS_PER_SYSTEM = FOLDS * EDITS_PER_FOLD_SIZE * SIZES
EDITS_ALL = N_SYSTEMS * EDITS_PER_SYSTEM
EDIT_PROPS_PER_SYSTEM = EDITS_PER_SYSTEM * PREDICTORS_PER_EDIT
BASELINE_PROPS_PER_SYSTEM = PREFIXES * CONTINUATIONS
S6_PROPS_PER_SYSTEM = EDIT_PROPS_PER_SYSTEM + BASELINE_PROPS_PER_SYSTEM
S6_PROPS_ALL = N_SYSTEMS * S6_PROPS_PER_SYSTEM
O2_FLOAT = PREFIXES * CONTINUATIONS * 3 * 2
FLOAT_MAX = S6_PROPS_ALL + O2_FLOAT
EXACT_O1 = PREFIXES + (PREFIXES * CONTINUATIONS)
FITS_PER_SYSTEM = FOLDS * (2 + 2 * CLASSES)
FITS_ALL = N_SYSTEMS * FITS_PER_SYSTEM
NC1_REFIT = 1
B3_STACKS = 4 * (FOLDS + FOLDS * CLASSES)
SVDS = FITS_ALL + NC1_REFIT + B3_STACKS
LOSS_CELLS_PER_FIT_TYPE = FOLDS * CLASSES * 2 * GROUPS * SIZES
LOSS_RECORDS = N_SYSTEMS * FIT_TYPES * MODES * LOSS_CELLS_PER_FIT_TYPE
POOLED = N_SYSTEMS * FIT_TYPES * GROUPS * SIZES * MODES
COVERAGE = N_SYSTEMS * (FOLDS * SIZES + FOLDS * CLASSES * SIZES)
IDENTITY_CELLS = 150 + 108 + 120 + 660 + 72 + 12 + 6
GUARD_RECORDS = 120 + 96 + 240

STAGES = ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8")
UNITS = ("propagation", "fit", "b3_stack")

_EXPECTED = {
    "EDITS_PER_FOLD_SIZE": 4096,
    "EDITS_PER_FOLD_CLASS_SIZE": 1024,
    "EDITS_PER_SYSTEM": 98304,
    "EDITS_ALL": 688128,
    "S6_PROPS_PER_SYSTEM": 491776,
    "S6_PROPS_ALL": 3442432,
    "O2_FLOAT": 1536,
    "FLOAT_MAX": 3443968,
    "EXACT_O1": 272,
    "FITS_PER_SYSTEM": 60,
    "FITS_ALL": 420,
    "B3_STACKS": 120,
    "SVDS": 541,
    "LOSS_CELLS_PER_FIT_TYPE": 576,
    "LOSS_RECORDS": 16128,
    "POOLED": 336,
    "COVERAGE": 840,
    "IDENTITY_CELLS": 1128,
    "GUARD_RECORDS": 456,
}


def schedule_drift() -> str | None:
    """Return a reason when the frozen products drifted. None means they match.

    Called from stage S0. It does not run at import.
    """
    actual = {
        "EDITS_PER_FOLD_SIZE": EDITS_PER_FOLD_SIZE,
        "EDITS_PER_FOLD_CLASS_SIZE": EDITS_PER_FOLD_CLASS_SIZE,
        "EDITS_PER_SYSTEM": EDITS_PER_SYSTEM,
        "EDITS_ALL": EDITS_ALL,
        "S6_PROPS_PER_SYSTEM": S6_PROPS_PER_SYSTEM,
        "S6_PROPS_ALL": S6_PROPS_ALL,
        "O2_FLOAT": O2_FLOAT,
        "FLOAT_MAX": FLOAT_MAX,
        "EXACT_O1": EXACT_O1,
        "FITS_PER_SYSTEM": FITS_PER_SYSTEM,
        "FITS_ALL": FITS_ALL,
        "B3_STACKS": B3_STACKS,
        "SVDS": SVDS,
        "LOSS_CELLS_PER_FIT_TYPE": LOSS_CELLS_PER_FIT_TYPE,
        "LOSS_RECORDS": LOSS_RECORDS,
        "POOLED": POOLED,
        "COVERAGE": COVERAGE,
        "IDENTITY_CELLS": IDENTITY_CELLS,
        "GUARD_RECORDS": GUARD_RECORDS,
    }
    if actual != _EXPECTED:
        return "schedule arithmetic drifted"
    if FLOAT_MAX != SCHEDULED_FLOAT or EXACT_O1 != DECLARED_N_O1:
        return "schedule does not match pinned maxima"
    if len(SYSTEM_ORDER) != N_SYSTEMS:
        return "system count drifted"
    return None


def check_schedule_arithmetic() -> None:
    """S0. A drifted schedule is INTEGRITY STOP (RL-8)."""
    reason = schedule_drift()
    if reason is not None:
        integrity_stop(reason)


def scheduled_count(system: str, stage: str, unit: str) -> int:
    """One cell of the 7 × 9 × 3 accounting grid.

    Package-level exact calls and O2 float calls are attributed to SYS-O6
    because 272 and 1,536 are not divisible by 7. See the conformance note
    CI-ACCOUNTING-ATTRIBUTION. Summing the grid recovers the package maxima.
    """
    if system not in SYSTEM_ORDER or stage not in STAGES or unit not in UNITS:
        integrity_stop("schedule key is not in the frozen grid", system=system, stage=stage, unit=unit)
    if unit == "propagation" and stage == "S1" and system == "SYS-O6":
        return EXACT_O1
    if unit == "propagation" and stage == "S2" and system == "SYS-O6":
        return O2_FLOAT
    if unit == "propagation" and stage == "S6":
        return S6_PROPS_PER_SYSTEM
    if unit == "fit" and stage == "S3" and system == "SYS-NC1":
        return NC1_REFIT
    if unit == "fit" and stage == "S5":
        return FITS_PER_SYSTEM
    if unit == "b3_stack" and stage == "S5" and system in B3_SYSTEMS:
        return FOLDS + FOLDS * CLASSES
    return 0


def grid_sum(unit: str, stage: str | None = None) -> int:
    total = 0
    for system in SYSTEM_ORDER:
        for name in STAGES:
            if stage is not None and name != stage:
                continue
            total += scheduled_count(system, name, unit)
    return total
