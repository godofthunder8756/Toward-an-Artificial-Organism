"""Appendix A wider tuned-rival grid. Frozen, not approved, not executed.

The study entry point raises before any training. The grid, tie-break, and the
training loop are here so the hashed text fixes the design before exposure.
"""

from __future__ import annotations

import math

from graded_reversion_spec import (
    APPENDIX_A_APPROVED,
    EDGE_LIMITED,
    EPS0,
    GRID_QUALIFIER,
)
from recurrent_core_transfer_spec import ADVANTAGE_NOT, ADVANTAGE_OBSERVED, RIVAL_AFIT, RIVAL_AFIT_NOT

ORIGINAL_G = (0.5, 1.0, 2.0)
ORIGINAL_B = (-2.0, 0.0, 2.0)
EXTENSION_G = (
    1.0,
    math.sqrt(2.0),
    2.0,
    2.0 * math.sqrt(2.0),
    4.0,
    4.0 * math.sqrt(2.0),
    8.0,
)
EXTENSION_B = (-6.0, -4.0, -3.0, -2.0, -1.0, 0.0)


class AppendixNotApproved(RuntimeError):
    """Appendix A needs its own approval. This study does not have it."""


def _key(g: float, b: float) -> tuple[float, float]:
    return (round(float(g), 12), round(float(b), 12))


def rival_grid() -> list[dict]:
    """Union of the original 9 and the 42-point extension: 47 configurations."""
    configs = {}
    for g in ORIGINAL_G:
        for b in ORIGINAL_B:
            configs[_key(g, b)] = {"g": float(g), "b": float(b), "origin": "original"}
    for g in EXTENSION_G:
        for b in EXTENSION_B:
            key = _key(g, b)
            if key in configs:
                configs[key] = {"g": float(g), "b": float(b), "origin": "overlap"}
            else:
                configs[key] = {"g": float(g), "b": float(b), "origin": "extension"}
    rows = list(configs.values())
    rows.sort(key=lambda row: (row["g"], row["b"]))
    return rows


def select_rival(rows: list[dict]) -> tuple[dict, bool]:
    """Minimum VAL criterion, then the ε₀ band, then the Appendix A tie-break."""
    if len(rows) != 47:
        raise ValueError("expected 47 configurations, got %d" % len(rows))
    best = min(row["criterion"] for row in rows)
    tied = [row for row in rows if row["criterion"] - best <= EPS0]

    def key(row: dict):
        g = row["g"]
        b = row["b"]
        return (abs(math.log2(g)), abs(b), b, g)

    chosen = min(tied, key=key)
    return chosen, len(tied) > 1


def is_boundary(g: float, b: float) -> bool:
    return bool(g == 8.0 or b == -6.0)


def is_reported_original_edge(g: float, b: float) -> bool:
    """Selections at g = 0.5 or b = +2 are reported."""
    return bool(g == 0.5 or b == 2.0)


def boundary_label(pairs: list[tuple[float, float]]) -> str | None:
    if len(pairs) != 10:
        raise ValueError(len(pairs))
    hits = sum(1 for g, b in pairs if is_boundary(g, b))
    if hits >= 3:
        return EDGE_LIMITED
    return None


def advantage_label(passed: bool) -> str:
    base = ADVANTAGE_OBSERVED if passed else ADVANTAGE_NOT
    return "%s %s" % (base, GRID_QUALIFIER)


def rival_afit_label(passed: bool) -> str:
    base = RIVAL_AFIT if passed else RIVAL_AFIT_NOT
    return "%s %s" % (base, GRID_QUALIFIER)


def run_appendix_a(*_args, **_kwargs):
    """Study entry point. Always refuses."""
    raise AppendixNotApproved(
        "Appendix A is not approved. The wider rival grid must not be run."
    )


def execute_appendix_a_training(seeds, inits, world, directory, steps: int = 4000):
    """Full Appendix A loop. Unreachable while APPENDIX_A_APPROVED is false.

    Selection uses an 8→70→3 readout from torch seed 6000+s and rejects TEST and
    VAL. The refit on the 192 TRAIN histories is R-TUNED843 (8→70→3, seed
    6000+s) and F-TUNED32 (8→32→3, seed 5000+s).
    """
    if not APPENDIX_A_APPROVED:
        raise AppendixNotApproved(
            "Appendix A is not approved. The wider rival grid must not be run."
        )

    from recurrent_core_transfer_metrics import predict_histories, probability_excess, val_histories
    from recurrent_core_transfer_models import build_initialized, copy_recurrent, snapshot_state, tune_recurrent
    from recurrent_core_transfer_train import train_arm

    histories = val_histories()
    directory.mkdir(parents=True, exist_ok=True)
    records = []
    for seed in seeds:
        w0 = inits[seed]
        grid_rows = []
        for spec in rival_grid():
            model = build_initialized(6000 + seed, READOUT_70)
            copy_recurrent(model, tune_recurrent(w0, spec["g"], spec["b"]))
            info = train_arm(model, seed, True, True, steps=steps)
            if info["integrity_training"]:
                predictions = predict_histories(model, histories)
                criterion = probability_excess(predictions, histories, world)["total"]
            else:
                criterion = float("inf")
            grid_rows.append(
                {
                    "g": spec["g"],
                    "b": spec["b"],
                    "origin": spec["origin"],
                    "criterion": criterion,
                    "training_ok": bool(info["integrity_training"]),
                    "state": snapshot_state(model),
                }
            )
        chosen, tie = select_rival(grid_rows)
        tuned = tune_recurrent(w0, chosen["g"], chosen["b"])
        rival = build_initialized(6000 + seed, READOUT_70)
        copy_recurrent(rival, tuned)
        rival_info = train_arm(rival, seed, True, False, steps=steps)
        tuned32 = build_initialized(5000 + seed, READOUT_32)
        copy_recurrent(tuned32, tuned)
        tuned32_info = train_arm(tuned32, seed, True, False, steps=steps)
        records.append(
            {
                "seed": int(seed),
                "g": chosen["g"],
                "b": chosen["b"],
                "tie": tie,
                "boundary": is_boundary(chosen["g"], chosen["b"]),
                "original_edge": is_reported_original_edge(chosen["g"], chosen["b"]),
                "rival_training_ok": bool(rival_info["integrity_training"]),
                "f_tuned32_training_ok": bool(tuned32_info["integrity_training"]),
                "rival_state": snapshot_state(rival),
                "f_tuned32_state": snapshot_state(tuned32),
            }
        )
    return records
