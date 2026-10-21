"""E3-v2 ratio rule. Additive. The frozen E3 rule is not modified.

For a ratio N/D:
- D <= 1e-12 and N > 1e-12 returns +inf
- D <= 1e-12 and N <= 1e-12 returns UNDEFINED, which never counts as a pass
- otherwise returns N/D

The same rule applies to every ratio statistic. The frozen study still uses
`_rho`, which returns no value whenever D <= 1e-12. This module does not
change that function or any recorded verdict.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from twostream_acquisition_spec import (
    E3_COMPLEMENT_MIN,
    E3_PARTIAL_MAX,
    E3_WRONG_MAX,
    RATIO_TIE,
)
from twostream_acquisition_verdicts import e3_label

E3_V2_TIE = 1e-12
RATIO_NAMES = ("partial", "complement", "wrong")
RATIO_KINDS = ("vector", "xor")


class UndefinedRatio:
    """Both numerator and denominator are at or below 1e-12.

    This object never satisfies a pass comparison.
    """

    def __repr__(self) -> str:
        return "UNDEFINED"

    def __str__(self) -> str:
        return "UNDEFINED"

    def __le__(self, other) -> bool:
        return False

    def __ge__(self, other) -> bool:
        return False

    def __lt__(self, other) -> bool:
        return False

    def __gt__(self, other) -> bool:
        return False

    def __eq__(self, other) -> bool:
        return other is self

    def __hash__(self) -> int:
        return id(self)


UNDEFINED = UndefinedRatio()


class UnauditableFromSaved(UndefinedRatio):
    """A frozen null ratio whose numerator was not stored.

    Distinct from UNDEFINED. Saved nulls do not say whether N exceeded 1e-12.
    """

    def __repr__(self) -> str:
        return "UNAUDITABLE_FROM_SAVED"

    def __str__(self) -> str:
        return "UNAUDITABLE_FROM_SAVED"


UNAUDITABLE_FROM_SAVED = UnauditableFromSaved()


def e3_v2_ratio(numerator: float, denominator: float):
    """Apply the consult #12 rule to one numerator and one denominator."""
    numerator = float(numerator)
    denominator = float(denominator)
    if not math.isfinite(numerator) or not math.isfinite(denominator):
        raise ValueError("E3-v2 requires finite numerator and denominator")
    if denominator <= E3_V2_TIE and numerator > E3_V2_TIE:
        return math.inf
    if denominator <= E3_V2_TIE and numerator <= E3_V2_TIE:
        return UNDEFINED
    return numerator / denominator


def e3_v2_meets(value, threshold: float, *, at_least: bool) -> bool:
    """Threshold check. UNDEFINED never passes. +inf passes only an at-least gate."""
    if value is UNDEFINED or value is UNAUDITABLE_FROM_SAVED:
        return False
    if at_least:
        return bool(value >= threshold)
    return bool(value <= threshold)


def e3_v2_from_saved(saved):
    """Map one frozen saved ratio onto E3-v2 without recovering N and D.

    The frozen function stores a float only when D > 1e-12. That is the same
    cutoff, so the stored float is already N/D under E3-v2. A stored null does
    not record N, so it stays unauditable. This function does not retrain.
    """
    if saved is None:
        return UNAUDITABLE_FROM_SAVED
    if isinstance(saved, bool) or not isinstance(saved, (int, float)):
        raise TypeError(type(saved).__name__)
    if not math.isfinite(saved):
        raise ValueError("saved ratio is not finite")
    if RATIO_TIE != E3_V2_TIE:
        raise RuntimeError("frozen tie cutoff and E3-v2 cutoff differ; saved identity does not hold")
    return float(saved)


def _gate(name: str, kind: str):
    if name == "complement":
        return E3_COMPLEMENT_MIN, True
    if name == "wrong" and kind == "xor":
        return E3_WRONG_MAX, False
    return E3_PARTIAL_MAX, False


def localized_from_saved_ratios(ratios) -> bool:
    """E3-v2 reading of a saved partial/complement/wrong block."""
    if not isinstance(ratios, dict):
        return False
    checks = []
    for name in RATIO_NAMES:
        block = ratios.get(name) or {}
        for kind in RATIO_KINDS:
            value = e3_v2_from_saved(block.get(kind))
            threshold, at_least = _gate(name, kind)
            checks.append(e3_v2_meets(value, threshold, at_least=at_least))
    return all(checks)


def _walk_ratio_leaves(obj, path, found):
    if isinstance(obj, dict):
        vector = obj.get("vector")
        xor = obj.get("xor")
        if "vector" in obj and "xor" in obj and not isinstance(vector, dict) and not isinstance(xor, dict):
            found.append((path, {"vector": vector, "xor": xor}))
        for key, value in obj.items():
            if key in ("vector", "xor") and not isinstance(value, dict):
                continue
            if key in ("rho_vector_vs_intended", "rho_xor_vs_intended") and not isinstance(value, dict):
                found.append((path + "." + key, value))
            else:
                _walk_ratio_leaves(value, path + "." + key, found)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            _walk_ratio_leaves(value, "%s[%d]" % (path, index), found)


def _localized_blocks(intervention):
    blocks = [("primary", intervention)]
    for name in ("all16", "pca"):
        block = intervention.get(name)
        if isinstance(block, dict) and "localized" in block:
            blocks.append((name, block))
    return blocks


def audit_saved_runs(runs_dir: Path) -> dict:
    """DESCRIPTIVE AUDIT of saved E3 statistics. Not a verdict change."""
    runs_dir = Path(runs_dir)
    files = sorted(runs_dir.glob("*.json"))
    ratio_components = 0
    unauditable = []
    localized_rows = []
    for path in files:
        record = json.loads(path.read_text())
        intervention = record.get("interventions") or {}
        leaves = []
        _walk_ratio_leaves(intervention, "interventions", leaves)
        for leaf_path, leaf in leaves:
            if isinstance(leaf, dict):
                for kind in RATIO_KINDS:
                    ratio_components += 1
                    mapped = e3_v2_from_saved(leaf.get(kind))
                    if mapped is UNAUDITABLE_FROM_SAVED:
                        unauditable.append("%s:%s.%s" % (path.name, leaf_path, kind))
            else:
                ratio_components += 1
                mapped = e3_v2_from_saved(leaf)
                if mapped is UNAUDITABLE_FROM_SAVED:
                    unauditable.append("%s:%s" % (path.name, leaf_path))
        for block_name, block in _localized_blocks(intervention):
            saved_flag = bool(block.get("localized"))
            if isinstance(block.get("ratios"), dict):
                v2_flag = localized_from_saved_ratios(block["ratios"])
                source = "saved ratios"
            else:
                v2_flag = saved_flag
                source = "no saved ratio block; flag left as recorded"
            localized_rows.append(
                {
                    "file": path.name,
                    "arm": record.get("arm"),
                    "seed": record.get("seed"),
                    "block": block_name,
                    "saved_localized": saved_flag,
                    "e3v2_localized": v2_flag,
                    "differs": saved_flag != v2_flag,
                    "source": source,
                    "integrity": bool(record.get("integrity")),
                    "coverage_ok": bool(block.get("coverage_ok")) if block_name == "primary" else None,
                    "rank_ok": bool(block.get("rank_ok")) if block_name == "primary" else None,
                    "descriptive_only": bool(block.get("descriptive_only")),
                }
            )
    differs = [row for row in localized_rows if row["differs"]]
    source_counts = {}
    for row in localized_rows:
        source_counts[row["source"]] = source_counts.get(row["source"], 0) + 1
    gru8_primary = []
    for path in files:
        if not path.name.startswith("cand_gru8_"):
            continue
        record = json.loads(path.read_text())
        ratios = (record.get("interventions") or {}).get("ratios") or {}
        gru8_primary.append(
            {
                "seed": record["seed"],
                "partial_vector": ratios["partial"]["vector"],
                "partial_xor": ratios["partial"]["xor"],
                "complement_vector": ratios["complement"]["vector"],
                "complement_xor": ratios["complement"]["xor"],
                "wrong_vector": ratios["wrong"]["vector"],
                "wrong_xor": ratios["wrong"]["xor"],
            }
        )
    gru8_primary.sort(key=lambda row: row["seed"])

    def study_rows(arm, freeze_name):
        chosen = [
            row for row in localized_rows
            if row["block"] == "primary" and row["arm"] == arm and freeze_name(row["file"])
        ]
        chosen.sort(key=lambda row: row["seed"])
        return chosen

    def packed(rows, key):
        return [
            {
                "localized": bool(row[key]) and bool(row["integrity"]),
                "coverage_ok": bool(row["coverage_ok"]),
                "rank_ok": bool(row["rank_ok"]),
            }
            for row in rows
        ]

    cand = study_rows("CAND", lambda name: name.startswith("cand_gru8_"))
    kfr = study_rows("K-FR", lambda name: name.startswith("kfr_gru8_"))
    saved_e3 = e3_label(packed(cand, "saved_localized"))
    v2_e3 = e3_label(packed(cand, "e3v2_localized"))
    saved_kfr = e3_label(packed(kfr, "saved_localized"))
    v2_kfr = e3_label(packed(kfr, "e3v2_localized"))
    return {
        "label": "DESCRIPTIVE AUDIT, NOT A VERDICT CHANGE",
        "runs": len(files),
        "ratio_components": ratio_components,
        "unauditable_from_saved": unauditable,
        "localized_flags": len(localized_rows),
        "localized_flags_that_differ": len(differs),
        "localized_flag_sources": source_counts,
        "differing_flags": differs,
        "gru8_cand_primary_ratios": gru8_primary,
        "gru8_cand_saved_e3": saved_e3,
        "gru8_cand_e3v2_e3": v2_e3,
        "gru8_kfr_saved_e3": saved_kfr,
        "gru8_kfr_e3v2_e3": v2_kfr,
        "any_label_would_differ": bool(differs) or saved_e3 != v2_e3 or saved_kfr != v2_kfr,
        "frozen_tie_equals_v2_tie": RATIO_TIE == E3_V2_TIE,
    }
