"""Corrected K-EXACT precision curve. Additive. The frozen function stays.

`quantized_exact_forecasts` in `twostream_acquisition_metrics.py` quantizes the
post-transition chart against post-observation ranges. This module applies the
transition to the previous repaired chart, then observes, then quantizes the
post-observation chart against those same ranges. No neural training.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from twostream_acquisition_metrics import (
    _observe_f,
    _prefix_chart,
    _repair,
    _transit_f,
    afit_holds,
    component_excess,
    exact_ranges,
    quantize_coordinates,
    quantized_exact_forecasts,
)
from twostream_acquisition_spec import B_GRID, CONSTANT_SPAN

FROZEN_METRICS = Path(__file__).resolve().parent / "twostream_acquisition_metrics.py"
FROZEN_METRICS_SHA256 = "bb7f0440d08ea52faf01dc0e1764189a3f4629a991e60a08ff9cbb465abc5302"


def frozen_metrics_sha256() -> str:
    return hashlib.sha256(FROZEN_METRICS.read_bytes()).hexdigest()


def quantized_exact_forecasts_v2(ranges, bits: int):
    """Post-observation quantization of the exact chart.

    Per reading: transition the previous repaired chart (skipped before the
    first reading), observe, quantize against the post-observation range,
    then repair. The retained state is still the three quantization indices.
    Feeding those indices forward can push a later TRAIN chart outside the
    exact TRAIN box by more than float32 endpoint rounding. That extra
    overshoot shrinks as the bit width grows. It is separate from the
    phase-mismatch clip in the frozen function.
    Returns forecasts, repair counts, clip counts, the maximum positive
    overshoot over all histories, and the pre-quantization charts.
    """
    predictions = np.zeros((256, 3), dtype=np.float64)
    repairs = np.zeros(8, dtype=np.int64)
    clips = np.zeros(8, dtype=np.int64)
    overshoot = np.zeros(8, dtype=np.float64)
    preclip = np.zeros((256, 8, 3), dtype=np.float64)
    for history in range(256):
        mx, my, c = 0.5, 0.5, 0.0
        for stage in range(8):
            bit = (history >> stage) & 1
            variable = "X" if stage % 2 == 0 else "Y"
            if stage > 0:
                mx, my, c = _transit_f(mx, my, c)
            mx, my, c = _observe_f(mx, my, c, variable, bit)
            chart = np.array([mx, my, c], dtype=np.float64)
            preclip[history, stage] = chart
            lo, hi = ranges[stage]
            overshoot[stage] = max(
                overshoot[stage],
                float(np.max(np.maximum(lo - chart, 0.0))),
                float(np.max(np.maximum(chart - hi, 0.0))),
            )
            reconstructed, outside, _constant = quantize_coordinates(chart, lo, hi, bits)
            clips[stage] += int(np.sum(outside))
            mx, my, c, changed = _repair(
                float(reconstructed[0]), float(reconstructed[1]), float(reconstructed[2])
            )
            repairs[stage] += int(changed)
        qxor = mx + my - 2.0 * (mx * my + c)
        predictions[history] = (mx, my, qxor)
    return predictions, repairs.tolist(), clips.tolist(), overshoot.tolist(), preclip


def _split_mask(world, test: bool) -> np.ndarray:
    mask = np.asarray(world.is_test, dtype=bool)
    return mask if test else ~mask


def exact_phase_overshoot(world) -> dict:
    """Overshoot of exact, unquantized charts against post-observation ranges.

    Frozen order quantizes the post-transition chart at readings 1–7.
    Corrected order quantizes the post-observation chart at every reading.
    """
    ranges = exact_ranges(world)
    out = {"frozen_order": {}, "corrected_order": {}}
    for label, test in (("TRAIN", False), ("TEST", True)):
        histories = np.flatnonzero(_split_mask(world, test))
        frozen = []
        corrected = []
        for stage in range(8):
            frozen_max = 0.0
            corrected_max = 0.0
            lo, hi = ranges[stage]
            for history in histories:
                post = _prefix_chart(int(history), stage + 1)
                corrected_max = max(
                    corrected_max,
                    float(np.max(np.maximum(lo - post, 0.0))),
                    float(np.max(np.maximum(post - hi, 0.0))),
                )
                if stage < 7:
                    tx, ty, tc = _transit_f(float(post[0]), float(post[1]), float(post[2]))
                    chart = np.array([tx, ty, tc], dtype=np.float64)
                else:
                    chart = post
                frozen_max = max(
                    frozen_max,
                    float(np.max(np.maximum(lo - chart, 0.0))),
                    float(np.max(np.maximum(chart - hi, 0.0))),
                )
            frozen.append(frozen_max)
            corrected.append(corrected_max)
        out["frozen_order"][label] = frozen
        out["corrected_order"][label] = corrected
    return out


def _constant_mask(ranges):
    return [(hi - lo < CONSTANT_SPAN) for lo, hi in ranges]


def _stagewise_bits(ranges, bits: int):
    return [int((~np.asarray(mask)).sum()) * bits for mask in _constant_mask(ranges)]


def _split_overshoot(preclip: np.ndarray, ranges, mask: np.ndarray) -> list:
    values = []
    for stage in range(8):
        lo, hi = ranges[stage]
        charts = preclip[mask, stage]
        if charts.size == 0:
            values.append(0.0)
            continue
        excess = np.maximum(lo - charts, 0.0)
        excess = np.maximum(excess, charts - hi)
        values.append(float(np.max(excess)))
    return values


def _max_abs_delta(forecasts, world, test: bool) -> float:
    mask = _split_mask(world, test)
    if not np.any(mask):
        return None
    return float(np.max(np.abs(forecasts[mask] - world.q[mask])))


def kexact_precision_v2(world) -> dict:
    """Same selection rule as the frozen reference report, on the corrected curve."""
    ranges = exact_ranges(world)
    curve = []
    selected = None
    test_selected = None
    for bits in B_GRID:
        forecasts, repairs, clips, overshoot, preclip = quantized_exact_forecasts_v2(ranges, bits)
        valid = bool(np.isfinite(forecasts).all())
        errors = component_excess(forecasts, world) if valid else None
        train_afit = bool(valid and afit_holds(errors, world, "TRAIN"))
        test_afit = bool(valid and afit_holds(errors, world, "TEST"))
        curve.append(
            {
                "b": bits,
                "train_afit": train_afit,
                "test_afit": test_afit,
                "errors": errors,
                "repairs": repairs,
                "clip_counts": clips,
                "max_clip_overshoot": overshoot,
                "max_clip_overshoot_train": _split_overshoot(preclip, ranges, _split_mask(world, False)),
                "max_clip_overshoot_test": _split_overshoot(preclip, ranges, _split_mask(world, True)),
                "max_abs_delta_q": {
                    "TRAIN": _max_abs_delta(forecasts, world, False),
                    "TEST": _max_abs_delta(forecasts, world, True),
                },
            }
        )
        if train_afit and selected is None:
            selected = bits
        if test_afit and test_selected is None:
            test_selected = bits
    constant = [mask.tolist() if hasattr(mask, "tolist") else [bool(v) for v in mask] for mask in _constant_mask(ranges)]
    if selected is None:
        confirmation = "NOT CONFIRMED"
        b_sel = "no qualifying precision in the declared grid"
        stagewise = None
        nominal = None
    else:
        chosen = next(row for row in curve if row["b"] == selected)
        confirmation = "CONFIRMED" if chosen["test_afit"] else "NOT CONFIRMED"
        b_sel = selected
        stagewise = _stagewise_bits(ranges, selected)
        nominal = 3 * selected
    return {
        "ordering": "transition previous repaired chart, observe, quantize post-observation chart",
        "function": "quantized_exact_forecasts_v2",
        "frozen_function_unchanged": "twostream_acquisition_metrics.quantized_exact_forecasts",
        "frozen_metrics_sha256": frozen_metrics_sha256(),
        "b_grid": list(B_GRID),
        "b_sel_train": b_sel,
        "smallest_passing_precision_train": selected,
        "smallest_passing_precision_test": test_selected,
        "confirmation": confirmation,
        "charged_state_bits_nominal": nominal,
        "charged_state_bits_stagewise": stagewise,
        "ranges_constant": constant,
        "metadata_bits": 64 * 3 * 8,
        "curve": curve,
        "exact_unquantized_overshoot": exact_phase_overshoot(world),
        "thresholds": {
            "TRAIN": {
                "total": float(world.afit_threshold["TRAIN"]["total"]),
                "XOR": float(world.afit_threshold["TRAIN"]["XOR"]),
            },
            "TEST": {
                "total": float(world.afit_threshold["TEST"]["total"]),
                "XOR": float(world.afit_threshold["TEST"]["XOR"]),
            },
        },
    }


def frozen_curve_matches_reference(world, reference: dict) -> bool:
    """Provenance: the untouched frozen function still matches reference_arms.json."""
    ranges = exact_ranges(world)
    recorded = reference["K-EXACT"]["precision"]["curve"]
    if len(recorded) != len(B_GRID):
        return False
    for bits, row in zip(B_GRID, recorded):
        forecasts, repairs, clips = quantized_exact_forecasts(ranges, bits)
        errors = component_excess(forecasts, world)
        if row["b"] != bits or repairs != row["repairs"] or clips != row["clip_counts"]:
            return False
        for split in ("TRAIN", "TEST"):
            for key in ("X", "Y", "XOR", "total"):
                if errors[split][key] != row["errors"][split][key]:
                    return False
    return True


def write_report(path: Path, world) -> dict:
    report = kexact_precision_v2(world)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    return report
