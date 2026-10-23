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


# RL-4 memory budget. These integers are not keys of FROZEN_RUNTIME.
# Annex v2 row 6 omitted the fitted matrices, the normal-equation terms and
# the label records. Row 7 is the serialization of row 6, so those records
# add serialization as well. The factor of 2 is the annex v2 arena allowance.
# The RLIMIT_AS comparison uses VmPeak plus this budget. RSS is not an input.
ANNEX_V2_INCREMENTAL_BYTES = 149_066_512
RECORD_BUDGET_BYTES = 2048
SERIALIZATION_BYTES_PER_RECORD = 4096
FITTED_MATRIX_RECORDS = 420
NORMAL_EQUATION_PREFIX_G = 112
NORMAL_EQUATION_PREFIX_R = 112
NORMAL_EQUATION_FOLD_TERMS = 840
NORMAL_EQUATION_RECORDS = NORMAL_EQUATION_PREFIX_G + NORMAL_EQUATION_PREFIX_R + NORMAL_EQUATION_FOLD_TERMS
LABEL_ROWS = 7 * 2 * 2
VALIDATION_RECORDS = 1
HEADROOM_RECORDS = 1
LABEL_RECORDS = LABEL_ROWS + VALIDATION_RECORDS + HEADROOM_RECORDS
ADDED_MEMORY_RECORDS = FITTED_MATRIX_RECORDS + NORMAL_EQUATION_RECORDS + LABEL_RECORDS
ADDED_RECORD_BYTES = ADDED_MEMORY_RECORDS * RECORD_BUDGET_BYTES
ADDED_SERIALIZATION_BYTES = ADDED_MEMORY_RECORDS * SERIALIZATION_BYTES_PER_RECORD
INCREMENTAL_BYTES = ANNEX_V2_INCREMENTAL_BYTES + ADDED_RECORD_BYTES + ADDED_SERIALIZATION_BYTES
PACKAGE_BUDGET_BYTES = INCREMENTAL_BYTES * 2

# Sealed oracle artifacts from PR #13. The post-run index re-hashes these and
# records the comparison. A mismatch does not stop (RL-5).
ORACLE_SEALED_MANIFEST_SHA256 = "4179b71a0110903472d6506686b2f7e0ab2188d9050c9c3f40c31a2fb6b46831"
ORACLE_SEALED_OUTPUT_SHA256 = {
    "outputs/REPORT.md": "6c6d42ccefa224ec2e94a77f9f9c6169c318abee1db89decb4d0335a987e0785",
    "outputs/drawn_array_hashes.json": "ce286f281d7ee2989657e59c2d474d122ecaf21537270999f63f299279aac2ce",
    "outputs/drawn_arrays.npz": "1e7a599229cff0a1a61391b791139f30eff4f3a007007ba8de6a2e9177a0dea4",
    "outputs/fit_freeze_O6.json": "b6f817c8b3e70ae78e405f57e27226b08d1daec8fdbce7b2a1348a4c119e454a",
    "outputs/fit_freeze_O7.json": "347bcd511fe94648751473d182ed5118b2e57e04207ee5b3e4f1385e8c16bd05",
    "outputs/results.json": "6adb5de2650f5017b3f4195c84cf4b6955abb94186a01c92795efe0717dd0023",
    "outputs/run.log": "64f9af66c9b4154b314e08b10663f8e479fd323de6fb0af9812e35921b0a8977",
    "outputs/stage_O1.json": "794746a728caf4ff6211e6612ce007ae6f670084f2f4df898bc7ea3af692c3ec",
    "outputs/stage_O2.json": "4220a4df77511f48745a95f46064293ebff4d22b1368b435fbb102bb9c4818f1",
    "outputs/stage_O3.json": "2e30e9ad027fa4c5718a2e2b81a482429c3520b39ac215121ab26b96134a6539",
    "outputs/stage_O4.json": "7213d1709d8409dd7f49874f5fcb1a97e32dc58a8396316743d66f27cc918b3d",
    "outputs/stage_O5.json": "c61f6639a348542928fecdb82823b35928f56820626114973800c28f000c03ad",
    "outputs/stage_O6.json": "1a894f14501a19f783f50d13f4718f0ea45f32b77f9a810ada7da5147a9705b8",
    "outputs/stage_O7.json": "994dda0a1e9f4194726abab2420033c8ae266c8802bcf962f7a38ce7c2350116",
    "outputs/stop_kind.json": "2d5e1da5d451ba9addbafd9815b93163427c618d25732038531e07e49b6eb19a",
}


def oracle_rehash_row(found: str | None, expected: str) -> dict:
    """One sealed-artifact comparison. match may be false. stops is always false."""
    return {
        "sha256": found,
        "expected_sha256": expected,
        "match": found == expected,
        "stops": False,
    }


def fnum(key: str) -> float:
    return float(FROZEN_RUNTIME[key])
