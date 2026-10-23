"""Frozen constants for the recurrent-compensation study.

No consciousness claim. Below C4. This module does not train.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

PROTOCOL_FILENAME = "frozen_recurrent_compensation_protocol_FINAL.md"
PROTOCOL_SHA256 = "eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40"
APPROVAL_FILENAME = "FROZEN_RECURRENT_COMPENSATION_APPROVAL.md"
DEVIATIONS_FILENAME = "frozen_recurrent_compensation_DEVIATIONS.md"

SEEDS = tuple(range(400, 410))
ARMS = ("CAND", "R-FIX-32", "R-FIX-48")
ARM_HIDDEN = {"CAND": 32, "R-FIX-32": 32, "R-FIX-48": 48}
EXPECTED_COUNTS = {
    "CAND": {"trainable": 843, "stored": 843, "frozen": 0, "H": 32},
    "R-FIX-32": {"trainable": 651, "stored": 843, "frozen": 192, "H": 32},
    "R-FIX-48": {"trainable": 843, "stored": 1035, "frozen": 192, "H": 48},
}

TAU = 0.25
T_BOUNDARY_TOL = 1e-9
AGREEMENT_ABS = 1e-12
AGREEMENT_REL = 1e-9
PUBLISHED_PD = 0.013838622233977797

FIXTURE_SEED = 7
FIXTURE_DATA_SEED = 17
FIXTURE_STEPS = 4
FIXTURE_BATCH = 8

RESULTS_DIRNAME = "frozen_recurrent_compensation_results_v1"

PASS = "VERIFIED TARGET PASS"
FAIL = "VERIFIED TARGET FAIL"
BOUNDARY = "BOUNDARY / NUMERICALLY UNRESOLVED"
INVALID = "INVALID"
INTEGRITY = "INTEGRITY_FAILURE"

EXISTENCE_WITNESS = "WITNESS FOUND"
EXISTENCE_NOT_REACHED = "TARGET NOT REACHED WITHIN DECLARED SEARCH"
EXISTENCE_NONE = "NO VERIFIED WITNESS FOUND"

REPRO_YES = "TARGET REACHED REPRODUCIBLY"
REPRO_NO = "REPRODUCIBILITY CRITERION NOT MET"
REPRO_UNRESOLVED = "UNRESOLVED"

WITNESS_SENTENCE = (
    "For the reported W0 and head width H, a numerically verified GRU-8 checkpoint "
    "reaches the declared target while weight_hh remains at W0 throughout all eight updates. "
    "This is a counterexample to the claim that departing from that specified W0 is necessary "
    "for this target within the declared architecture. It does not establish success for other "
    "frozen matrices or negate the existing causal contribution of trained matrices in other implementations."
)
ACQUISITION_SENTENCE = (
    "The target was attained after training input weights, both biases and the readout, "
    "without training weight_hh."
)
REPRO_SENTENCE = (
    "At least eight of ten final checkpoints were verified target passes, establishing "
    "reproducibility within the declared search, not a logical minimum."
)
INIT_WITNESS_SENTENCE = (
    "This is an initialization witness. It demonstrates existence for that W0 and H, not acquisition."
)
SCOPE_SENTENCE = (
    "Earlier acquisition, transfer and exact-solution results are unchanged. This study can add "
    "restricted-class existence evidence and, where the initialization-to-final condition holds, "
    "evidence of acquired target attainment. It does not test transfer or add a new causal-organization claim."
)
TAU_DISCLOSURE = (
    "tau = 0.25 was chosen after prior results were known. Across the 30 existing CAND checkpoints "
    "(seeds 100–109, 200–209, 300–309), L_prefix/PD ranged 0.034–0.110, i.e. L_prefix/(0.25·PD) ≤ 0.44."
)
FINDING_4 = (
    "The XOR term determines T in all 30 existing CAND checkpoints. The prefix-loss constraint is "
    "satisfied with margin in those checkpoints. Which constraint limits R-FIX is unknown; all three "
    "target components remain decision-bearing."
)
FINDING_1 = (
    "R-FIX-32 tests compensation with the original architecture. R-FIX-48 additionally tests "
    "compensation with an equal total trainable-parameter count allocated differently. These "
    "comparisons do not isolate parameter count from readout width, parameter allocation or optimization effects."
)
FINDING_2 = (
    "Freeze only `weight_hh_l0`. Training W_ih and the biases can change the recurrent dynamics "
    "despite that fixed matrix. Do not describe R-FIX as having an entirely untrained or fixed recurrent computation."
)
G_PREFIX_NAME = "within-run prefix-loss improvement"
SHARED_INIT_NOTE = (
    "H = 32 initialization witnesses are shared by CAND and R-FIX-32 and counted once. "
    "The same count is noted under both arms."
)
SEARCH_SIZE = "The search size is 20 final R-FIX checkpoints plus their 20 inits."
NO_COMPARISON_TEST = (
    "There is no pooled R-FIX label and no comparison test between arms. "
    "R-FIX-32 vs R-FIX-48 differences are descriptive."
)
COMPARATOR_UNRESOLVED = "R-FIX-vs-CAND comparison: UNRESOLVED (comparator not reproduced)."

CODE_FILES = (
    PROTOCOL_FILENAME,
    APPROVAL_FILENAME,
    DEVIATIONS_FILENAME,
    "frozen_recurrent_compensation_spec.py",
    "frozen_recurrent_compensation_train.py",
    "frozen_recurrent_compensation_numpy_eval.py",
    "frozen_recurrent_compensation_eval.py",
    "frozen_recurrent_compensation_labels.py",
    "frozen_recurrent_compensation_study.py",
    "test_frozen_recurrent_compensation.py",
)

ROOT = Path(__file__).resolve().parent
COMPONENT_NAMES = ("prefix", "total", "xor")


def protocol_sha256() -> str:
    return hashlib.sha256((ROOT / PROTOCOL_FILENAME).read_bytes()).hexdigest()


def code_tree_sha256() -> str:
    """sha256 of sorted name, NUL, file sha256, newline. Manifests are not included."""
    digest = hashlib.sha256()
    for name in sorted(CODE_FILES):
        file_digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_digest.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def values_agree(x: float, y: float) -> bool:
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return False
    if isinstance(x, bool) or isinstance(y, bool):
        return False
    if not (math.isfinite(x) and math.isfinite(y)):
        return False
    return abs(float(x) - float(y)) <= AGREEMENT_ABS + AGREEMENT_REL * max(abs(float(x)), abs(float(y)))


def components_agree(left: dict, right: dict) -> bool:
    return all(values_agree(left[name], right[name]) for name in COMPONENT_NAMES)


def classify_T(t1: float, t2: float, agreed: bool) -> str:
    """§3.1. Agreement is required. Both evaluators must clear the same side of the gap around 1."""
    if not agreed or not (math.isfinite(t1) and math.isfinite(t2)):
        return INTEGRITY
    bound = T_BOUNDARY_TOL
    if t1 < 1.0 - bound and t2 < 1.0 - bound:
        return PASS
    if t1 > 1.0 + bound and t2 > 1.0 + bound:
        return FAIL
    return BOUNDARY


def not_reached_sentence(arm: str) -> str:
    return (
        "%s: TARGET NOT REACHED WITHIN DECLARED SEARCH (one run per seed, 4000 steps, PR #7 recipe, no restarts). "
        "Failure means only 'not reached within declared search.' This is not a necessity certificate and does not "
        "establish that departing from W0 is necessary."
        % arm
    )


def no_witness_sentence(arm: str, unresolved: int, invalid: int) -> str:
    return "%s: NO VERIFIED WITNESS FOUND (%d unresolved, %d invalid)." % (arm, unresolved, invalid)
