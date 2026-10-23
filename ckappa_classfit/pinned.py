"""Frozen runtime for the class-fit package.

Inherited keys are the ckappa_oracle.pinned.FROZEN_RUNTIME object, copied by
value. That module is not modified. Where v1.3 uses an inherited constant
unchanged, the inherited key is kept. This package's own propagation maximum
is a new key, classfit_scheduled_float_propagations (E39-6).
"""

from __future__ import annotations

from ckappa_oracle.pinned import FROZEN_RUNTIME as ORACLE_FROZEN_RUNTIME

PYTHON = ORACLE_FROZEN_RUNTIME["python"]
NUMPY = ORACLE_FROZEN_RUNTIME["numpy"]

# Package maximum under the inherited counting convention (E39-6, C8.3).
SCHEDULED_FLOAT = 3443968
DECLARED_N_O1 = 272
SCHEDULED_EXACT_REMAINING = 0

SYSTEM_ORDER = (
    "SYS-O6",
    "SYS-PC",
    "SYS-FK",
    "SYS-NC1",
    "SYS-NC2",
    "SYS-NC3",
    "SYS-LIM",
)
B3_SYSTEMS = ("SYS-FK", "SYS-NC1", "SYS-NC2", "SYS-NC3")
TRUE_CHART_SYSTEMS = ("SYS-O6", "SYS-PC", "SYS-LIM")
INADMISSIBLE_CANDIDATES = ("SYS-NC1", "SYS-NC2", "SYS-NC3")

# Consult #38 tolerances, verbatim (C5.5).
TOLERANCE_RECOVERY_ABS = "1e-9"
TOLERANCE_COMPARISON_ABS = "1e-12"
TOLERANCE_COMPARISON_REL = "1e-10"
TOLERANCE_CANCELLATION_ABS = "1e-12"
TOLERANCE_CANCELLATION_REL = "1e-10"
TOLERANCE_ZERO_GAIN_ABS = "1e-18"
TOLERANCE_ZERO_GAIN_REL = "1e-9"

# C4.5 frozen rational midpoint. The package recomputes t and compares exactly.
EXACT_T = "6299716077234553896/15613266622202707711"

ARRAY_COMMIT = "14376f38fe09157eef85bfac1cc4a4433d49bebc"
DRAWN_ARRAYS_FILE_SHA256 = "1e7a599229cff0a1a61391b791139f30eff4f3a007007ba8de6a2e9177a0dea4"
DRAWN_ARRAY_HASHES_FILE_SHA256 = "ce286f281d7ee2989657e59c2d474d122ecaf21537270999f63f299279aac2ce"
STAGE_O7_FILE_SHA256 = "994dda0a1e9f4194726abab2420033c8ae266c8802bcf962f7a38ce7c2350116"

# Per-array raw-byte sha256 (annex A1). Unused arrays are checked and not loaded into a fit.
RAW_ARRAY_SHA256 = {
    "Q": "01cdf2abcdefb52570c59c4ed227404d085704ab755df17e0ed25d729dfef919",
    "Q2": "86159ba687c89cd445164398e748464174b651acca27ecd111aa9599569b6937",
    "O6_directions": "5ed4bc8ba08bd9700bd9ad90c153301cf2fc7cc5c9a9b8f4477fb52ba0657c1d",
    "O4_directions": "6127c17d57d2dc4a795a0723165288f655bb1cc76f408090b2075ef8a3003e58",
    "O7_directions": "5ed4bc8ba08bd9700bd9ad90c153301cf2fc7cc5c9a9b8f4477fb52ba0657c1d",
}
USED_ARRAYS = ("Q", "Q2", "O6_directions")

SCOPE_SHA256 = "a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318"
ANNEX_V1_SHA256 = "8614bf114b127f4bdab516c0e933c23c84d1cd5f4d0ef34837d5cb0ad453d3a8"
CONSULT39_SHA256 = "e6403b63271af8c86ee8f159090a20c48c8c402a6832f6d63666fb3a03c89482"
CONSULT38_SHA256 = "87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5"
CONSULT37_SHA256 = "ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2"

FROZEN_RUNTIME = dict(ORACLE_FROZEN_RUNTIME)
FROZEN_RUNTIME.update(
    {
        "classfit_scheduled_float_propagations": SCHEDULED_FLOAT,
        "classfit_declared_n_o1": DECLARED_N_O1,
        "classfit_scheduled_exact_remaining": SCHEDULED_EXACT_REMAINING,
        "system_order": list(SYSTEM_ORDER),
        "matrix_forecast_recovery_max_abs": TOLERANCE_RECOVERY_ABS,
        "comparison_abs": TOLERANCE_COMPARISON_ABS,
        "comparison_rel": TOLERANCE_COMPARISON_REL,
        "cancellation_abs": TOLERANCE_CANCELLATION_ABS,
        "cancellation_rel": TOLERANCE_CANCELLATION_REL,
        "zero_gain_abs": TOLERANCE_ZERO_GAIN_ABS,
        "zero_gain_rel": TOLERANCE_ZERO_GAIN_REL,
        "summation_order_rho_c3": "sequential a=0..15",
        "exact_t": EXACT_T,
        "array_commit": ARRAY_COMMIT,
        "drawn_arrays_file_sha256": DRAWN_ARRAYS_FILE_SHA256,
        "stage_o7_file_sha256": STAGE_O7_FILE_SHA256,
        "svd_maximum": 541,
        "base_loss_record_maximum": 16128,
        "edit_maximum": 688128,
        "single_prefix_fits": 0,
    }
)


def fnum(key: str) -> float:
    return float(FROZEN_RUNTIME[key])
