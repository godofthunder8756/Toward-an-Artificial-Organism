"""A-SEP decision order from spec FINAL §4.5. Pure flag logic; no study quantities."""

from __future__ import annotations

CORE = ("C-REF", "C-T2", "C-SEL", "C-FO", "rescue")
_GAP = ("NOT APPLICABLE", "NOT EVALUABLE")


def conjunction_of(flags: dict) -> str:
    """FAIL outranks an unavailable criterion. UNAVAILABLE is not a pass."""
    if any(flags[k] == "FAIL" for k in CORE):
        return "FAILS"
    if any(flags[k] in _GAP or str(flags[k]).startswith("NOT EVALUABLE") or str(flags[k]).startswith("NOT APPLICABLE") for k in CORE):
        return "UNRESOLVED"
    if all(flags[k] == "PASS" for k in CORE):
        return "ATTAINED"
    return "UNRESOLVED"


def _failed(flags: dict) -> bool:
    return any(flags[k] == "FAIL" for k in CORE)


def _gap(flags: dict) -> bool:
    return any(
        flags[k] in _GAP or str(flags[k]).startswith("NOT EVALUABLE") or str(flags[k]).startswith("NOT APPLICABLE")
        for k in CORE
    )


def decide_setting(
    reference_met: bool,
    ref_flags: dict,
    controls: list,
    incomplete: bool = False,
    pm_undefined: bool = False,
):
    """Return (label, note) following the frozen decision order.

    `controls` entries need name, flags, reproduction, conjunction.
    """
    if incomplete:
        return ("UNRESOLVED-COMPUTE", "a required item is incomplete or NOT-RUN")
    if pm_undefined:
        return ("UNRESOLVED-DESIGN", "PM-ACT quotient is not well-defined")
    if _gap(ref_flags):
        missing = [k for k in CORE if ref_flags[k] in _GAP or str(ref_flags[k]).startswith("NOT")]
        return ("UNRESOLVED-DESIGN", "reference criterion undefined: " + ",".join(missing))
    if not reference_met:
        return ("REFERENCE CRITERIA NOT MET", "the reference does not meet the required conjunction")
    yes = [c["name"] for c in controls if c["reproduction"] == "YES"]
    if yes:
        return ("PATTERN REPRODUCED BY NAMED CONTROL", "reproducing: " + ", ".join(yes))
    attained = [c["name"] for c in controls if c["conjunction"] == "ATTAINED"]
    if attained:
        return (
            "CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED",
            "shared conjunction: " + ", ".join(attained),
        )
    gaps = [c["name"] for c in controls if (not _failed(c["flags"])) and _gap(c["flags"])]
    if gaps:
        return (
            "UNRESOLVED-DESIGN",
            "eligible control fails no evaluable core criterion while an essential comparison is unavailable: "
            + ", ".join(gaps),
        )
    if yes == [] and any(c["reproduction"] == "UNRESOLVED" for c in controls):
        names = [c["name"] for c in controls if c["reproduction"] == "UNRESOLVED"]
        return (
            "UNRESOLVED-DESIGN",
            "no reproduction is YES and some reproduction is UNRESOLVED: " + ", ".join(names),
        )
    if controls and all(_failed(c["flags"]) for c in controls):
        return (
            "DISTINGUISHES NAMED CONTROLS",
            "every eligible control fails at least one core criterion",
        )
    return ("UNRESOLVED-DESIGN", "no decision-order clause applied")
