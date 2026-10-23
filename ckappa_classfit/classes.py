"""Orbit, fold, and flip-class labels (v1.3 C3.1). Literal XOR rule."""

from __future__ import annotations

CLASS_ORDER = ("I", "X", "Y", "XY")
MASK_OF_CLASS = {"I": 0, "X": 5, "Y": 10, "XY": 15}
CLASS_OF_MASK = {0: "I", 5: "X", 10: "Y", 15: "XY"}
CHI = {"I": 1.0, "X": -1.0, "Y": -1.0, "XY": 1.0}
REPRESENTATIVE = {"A": 0, "B": 1, "C": 2, "D": 3}
FLIPS = (("X", 5), ("Y", 10), ("XY", 15))

# Declared table, C3.1. Used as the check against the XOR rule.
DECLARED_CLASS_PREFIXES = {
    "I": {"A": 0, "B": 1, "C": 2, "D": 3},
    "X": {"A": 5, "B": 4, "C": 7, "D": 6},
    "Y": {"A": 10, "B": 11, "C": 8, "D": 9},
    "XY": {"A": 15, "B": 14, "C": 13, "D": 12},
}

ORBITS = {
    "A": (0, 5, 10, 15),
    "B": (1, 4, 11, 14),
    "C": (2, 7, 8, 13),
    "D": (3, 6, 9, 12),
}

# (name, fit orbits, evaluation orbits), v1.1 listed order.
FOLD_SPEC = (
    ("AB->CD", ("A", "B"), ("C", "D")),
    ("CD->AB", ("C", "D"), ("A", "B")),
    ("AC->BD", ("A", "C"), ("B", "D")),
    ("BD->AC", ("B", "D"), ("A", "C")),
    ("AD->BC", ("A", "D"), ("B", "C")),
    ("BC->AD", ("B", "C"), ("A", "D")),
)

# D7 matrix cells: CD, BD and BC fitting folds (C4.5).
D7_FOLDS = ("CD->AB", "BD->AC", "BC->AD")

GROUP_INDEX = {"MARG": (0, 1), "XOR": (2,), "ALL": (0, 1, 2)}
GROUPS = ("ALL", "MARG", "XOR")


def prefixes_of(orbits) -> tuple:
    return tuple(sorted(prefix for name in orbits for prefix in ORBITS[name]))


def folds():
    return tuple(
        (name, prefixes_of(fit_orbits), prefixes_of(eval_orbits))
        for name, fit_orbits, eval_orbits in FOLD_SPEC
    )


def orbit_of_prefix() -> dict:
    found = {}
    for name, members in ORBITS.items():
        for prefix in members:
            found[prefix] = name
    return found


def class_of_prefix(orbit_of: dict | None = None) -> dict:
    orbits = orbit_of if orbit_of is not None else orbit_of_prefix()
    found = {}
    for prefix in range(16):
        mask = prefix ^ REPRESENTATIVE[orbits[prefix]]
        found[prefix] = CLASS_OF_MASK[mask]
    return found


def declared_matches_xor() -> bool:
    orbits = orbit_of_prefix()
    classes = class_of_prefix(orbits)
    for klass, row in DECLARED_CLASS_PREFIXES.items():
        for orbit, prefix in row.items():
            if classes[prefix] != klass or orbits[prefix] != orbit:
                return False
            if (prefix ^ REPRESENTATIVE[orbit]) != MASK_OF_CLASS[klass]:
                return False
    return True
