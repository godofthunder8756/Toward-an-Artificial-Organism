"""Matrix records and shared numeric helpers. No stage is run on import."""

from __future__ import annotations

import hashlib

import numpy as np

from ckappa_classfit.rankcats import rank_category_from_ratios


def matrix_sha(matrix: np.ndarray) -> str:
    raw = np.ascontiguousarray(matrix, dtype="<f8")
    return hashlib.sha256(raw.tobytes()).hexdigest()


def matrix_record(matrix: np.ndarray) -> dict:
    raw = np.ascontiguousarray(matrix, dtype="<f8")
    return {
        "values": raw.tolist(),
        "sha256": hashlib.sha256(raw.tobytes()).hexdigest(),
        "shape": [int(value) for value in raw.shape],
        "dtype": "<f8",
    }


def max_abs(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(matrix, dtype=np.float64))))


def diag3(x: float, y: float, k: float) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=np.float64)
    matrix[0, 0] = x
    matrix[1, 1] = y
    matrix[2, 2] = k
    return matrix


def rank_report_from_fit(system: str, fit_type: str, fold: str, klass, map_name: str, report: dict, n_rows: int, n_cols: int, empty: bool) -> dict:
    category = rank_category_from_ratios(
        report.get("ratios") if report else None,
        None if empty else (0.0 if report is None else report.get("sigma_1")),
        n_cols,
        empty,
    )
    return {
        "system": system,
        "fit_type": fit_type,
        "fold": fold,
        "class": klass,
        "map": map_name,
        "n_rows": n_rows,
        "n_cols": n_cols,
        "sigma": None if report is None else report.get("sigma"),
        "sigma_1": None if report is None else report.get("sigma_1"),
        "ratios": None if report is None else report.get("ratios"),
        "rank_category": category,
        "n_inverted": 0 if report is None else report.get("n_inverted"),
        "b3_status": None,
    }
