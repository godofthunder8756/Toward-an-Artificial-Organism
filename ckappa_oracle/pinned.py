"""Frozen runtime constants. Strings are the source for every float threshold.

The manifest's ``frozen_runtime`` object must equal ``FROZEN_RUNTIME``.
"""

PYTHON = "3.12.3"
NUMPY = "1.26.4"

# Integer schedule. Factors live in schedule.py; this integer is checked against it.
SCHEDULED_FLOAT = 788480
DECLARED_N_O1 = 272
SCHEDULED_EXACT_REMAINING = 0

FROZEN_RUNTIME = {
    "python": PYTHON,
    "numpy": NUMPY,
    "rcond": "1e-10",
    "guard": "1e-6",
    "fd_step": "1e-6",
    "o2_tolerance": "1e-8",
    "o6_tolerance": "1e-9",
    "boundary_relative": "1e-6",
    "coverage_fraction": "0.75",
    "all_sqrt_H": "1e-3",
    "all_R": "0.05",
    "marg_sqrt_H": "1e-4",
    "marg_R": "0.02",
    "reference_eps_syn": "0.1",
    "eps_syn": ["0.02", "0.05", "0.1", "0.25"],
    "o4_sizes": ["0.1", "0.25", "0.5"],
    "o4_direction_count": 64,
    "o6_direction_count": 16,
    "seed_Q": 35006,
    "seed_Q2": 35007,
    "seed_O6_directions": 35016,
    "seed_O4_directions": 35004,
    "memory_bytes": 4000000000,
    "hard_kill_seconds": 595,
    "soft_deadline_seconds": 540,
    "reserve_seconds": 60,
    "sample_propagations": 1000,
    "scheduled_float_propagations": SCHEDULED_FLOAT,
    "scheduled_exact_remaining": SCHEDULED_EXACT_REMAINING,
    "declared_n_o1": DECLARED_N_O1,
    "o7_void_stop_count": 5,
    "prefix_count": 16,
    "rank_resolved_above": "1e-6",
    "rank_resolved_zero_below": "1e-10",
    "o7_sigma3_stop_above": "1e-6",
    "input_commit": "5d9d8a7d1274d58e27e9a18380d1a33faaab57cc",
    "results_json_sha256": "bf2de92c9cd09809ad85145827922e9a70d6e742d30f8828d6c4973e92b51fed",
    "results_md_sha256": "8477e98c77860c61e997580a73d35d160711806d00b6789df55fe597b5b37a3c",
    "protocol_sha256": "6ff31a0dcecf123c7796fb2ba6fa4735c4efb7f968dbbcad19e46e4ff0151098",
    "certificate": "two-stream world-admission analytic certificate v1",
    "freeze_commit": "c69deb44b3c9ad06f176dae76fdaf311b992a665",
    "freeze_file_sha256": "c654a12176aebe0ab5ea4ee3c3b1e6a3c6167bd2b0df34b997fcaf28802dd280",
    "section6_seeds_prospective": [36000 + i for i in range(100, 110)],
}


def fnum(key: str) -> float:
    return float(FROZEN_RUNTIME[key])
