"""Constants for recurrent-core transfer. Thresholds are the protocol's.

Nothing here is retuned after TEST. Ambiguous readings are listed in
DEVIATIONS_AND_AMBIGUITIES.md and are not protocol edits.
"""

from __future__ import annotations

import math

PROTOCOL_SHA256 = "63c463c7b2df96d6feec49cfa34d1ec0f010ce017d4b31aab051f06af76e9506"
PROTOCOL_FILENAME = "RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md"

SEEDS = tuple(range(100, 110))
STEPS = 4000
BATCH = 256
LR_INIT = 1e-3
LR_FINAL = 1e-4
GRAD_CLIP = 1.0
ADAM_BETA1 = 0.9
ADAM_BETA2 = 0.999
ADAM_EPS = 1e-8

EPS0 = 1e-12
IDENTITY_TOL = 1e-9
A_FIT_FRACTION = 0.25
HALF = 0.5
QUARTER = 0.25
THREE_QUARTERS = 0.75
SHOWN_MIN = 8
INVALID_MAX = 2
N_RANDOM = 32
RIDGE_LAMBDA = 1e-3
CHART_R2_MIN = 0.9
ANGLE_MAX_DEG = 30.0
HIDDEN = 8
INPUT_SIZE = 9
READOUT_32 = 32
READOUT_70 = 70
RECURRENT_COUNT = 456
READOUT_32_COUNT = 387
TOTAL_843 = 843

GRID_G = (0.5, 1.0, 2.0)
GRID_B = (-2.0, 0.0, 2.0)
GATES = ("r", "z", "n")
GATE_ROWS = {"r": (0, 8), "z": (8, 16), "n": (16, 24)}
GATE_INDEX = {"r": 0, "z": 1, "n": 2}
CONTINUATION_STAGES = (4, 5, 6, 7)  # readings 5-8, 0-based
EARLY_STAGES = (0, 1, 2, 3)
P2_DRAWS = tuple(range(100))
P2_SCALES = (0.0, 0.03, 0.1, 0.3, 1.0)
P2_PIPELINE_SCALES = (0.0, 0.03)
KAPPA = 8.0
NUISANCE_SPECTRAL = 0.9

# Verbatim labels and claim sentences.
TRANSFER_SHOWN = "TRANSFER SHOWN"
TRANSFER_NOT_SHOWN = "TRANSFER NOT SHOWN"
UNRESOLVED = "UNRESOLVED"
E1_REPLICATED = "E1 REPLICATED"
E1_UNRESOLVED = "UNRESOLVED (E1 not replicated)"
ADVANTAGE_OBSERVED = "ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED"
ADVANTAGE_NOT = "not observed"
RIVAL_AFIT = "TUNED FROZEN GRU-8 MEETS A-FIT AT THIS BUDGET"
RIVAL_AFIT_NOT = "not met"
DECODER_OK = "DECODER PREDICTIVE AND CROSS-FOLD STABLE"
DECODER_NOT = "not met"
PIPELINE_OK = "PIPELINE VALID (E3-v2)"
PIPELINE_NOT = "PIPELINE NOT VALID (E3-v2)"
VARIATION_OK = "PREFIX VARIATION REDUCED WITH CONTINUATION VARIATION RETAINED"
VARIATION_FAIL = "selective variation reduction not demonstrated"

CLAIM_SUCCESS = (
    "In W2, recurrent training produced a GRU-8 core whose predictive advantage "
    "over its matched initialization survived replacement and retraining of the "
    "readout. For the specified matrix, reverting learned weights during "
    "continuation caused greater held-out prediction loss than each of 32 "
    "matched-norm random perturbations, meeting the prespecified materiality "
    "criterion in at least 8/10 fresh seeds."
)
CLAIM_FIRST_SENTENCE = (
    "In W2, recurrent training produced a GRU-8 core whose predictive advantage "
    "over its matched initialization survived replacement and retraining of the readout."
)
CLAIM_REVERSION_FAIL = (
    "Hidden-to-hidden matrix reversion did not meet the prespecified joint "
    "criterion for any matrix"
)
CLAIM_REVERSION_UNRESOLVED = "Hidden-to-hidden matrix reversion was UNRESOLVED"
Q7_TRANSFER = (
    "Transfer failure means transferable benefit was not demonstrated with this "
    "readout, optimization budget and split; it does not establish readout co-adaptation."
)
Q7_TUNED = (
    "Tuned-reservoir success establishes that the selected frozen alternative "
    "suffices under its declared resources; it does not explain away the candidate's "
    "learned contribution."
)
Q7_REVERSION = "the prespecified joint criterion was not met for any matrix"

VAL_LISTED = frozenset(
    {
        6, 10, 14, 21, 25, 29, 36, 40, 44, 51, 55, 59, 66, 70, 74, 81, 85, 89,
        96, 100, 104, 115, 119, 127, 130, 134, 142, 145, 149, 157, 160, 164, 172,
        179, 187, 191, 194, 202, 206, 209, 217, 221, 224, 232, 236, 247, 251, 255,
    }
)

CODE_FILES = (
    PROTOCOL_FILENAME,
    "DEVIATIONS_AND_AMBIGUITIES.md",
    "recurrent_core_transfer_spec.py",
    "recurrent_core_transfer_models.py",
    "recurrent_core_transfer_train.py",
    "recurrent_core_transfer_metrics.py",
    "recurrent_core_transfer_e3.py",
    "recurrent_core_transfer_p2.py",
    "recurrent_core_transfer_verdicts.py",
    "recurrent_core_transfer_study.py",
    "test_recurrent_core_transfer.py",
)


def is_val_history(history: int) -> bool:
    """VAL iff (p+u) mod 4 = 2 and u != (2-p) mod 16."""
    prefix = history % 16
    continuation = history // 16
    if (prefix + continuation) % 4 != 2:
        return False
    if continuation == (2 - prefix) % 16:
        return False
    return True


def foreign_seed(seed: int) -> int:
    """Cyclic pairing 100→101, …, 109→100."""
    return 100 + ((seed - 100 + 1) % 10)


def specific_name(gate: str, kind: str) -> str:
    if kind == "replicated":
        return "REPLICATED SPECIFIC(%s)" % gate
    if kind == "unresolved":
        return "UNRESOLVED(%s)" % gate
    if kind == "not":
        return "SPECIFIC(%s) NOT DEMONSTRATED" % gate
    raise ValueError(kind)


def is_grid_edge(g: float, b: float) -> bool:
    """The only interior grid point is (1, 0)."""
    return not (g == 1.0 and b == 0.0)


def select_configuration(rows: list[dict]) -> tuple[dict, bool]:
    """Min VAL criterion, then the protocol tie-break inside an ε₀ band."""
    if len(rows) != 9:
        raise ValueError(len(rows))
    best = min(row["criterion"] for row in rows)
    tied = [row for row in rows if row["criterion"] - best <= EPS0]

    def key(row: dict):
        g = row["g"]
        b = row["b"]
        return (abs(math.log2(g)), abs(b), b, g)

    chosen = min(tied, key=key)
    return chosen, len(tied) > 1
