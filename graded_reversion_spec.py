"""Constants for graded joint recurrent reversion.

Thresholds, seeds, doses, and claim sentences are the FINAL protocol's.
Nothing here is retuned after a phase A or phase B curve is seen.
Ambiguous readings are listed in graded_reversion_DEVIATIONS_AND_AMBIGUITIES.md.
"""

from __future__ import annotations

from recurrent_core_transfer_spec import (
    CONTINUATION_STAGES,
    EPS0,
    GATES,
    GATE_ROWS,
    HALF,
    IDENTITY_TOL,
    N_RANDOM,
    READOUT_32,
    READOUT_32_COUNT,
    READOUT_70,
    RECURRENT_COUNT,
    TOTAL_843,
)

PROTOCOL_FILENAME = "GRADED_REVERSION_PROTOCOL_FINAL.md"
PROTOCOL_SHA256 = "1a5e62bd034c579eed70d477251650aefdf1cd395834184bc564f5a16689bfa3"
DEVIATIONS_FILENAME = "graded_reversion_DEVIATIONS_AND_AMBIGUITIES.md"
FREEZE_FILENAME = "GRADED_REVERSION_FREEZE_v1.json"
APPROVAL_FILENAME = "GRADED_REVERSION_PHASE_B_APPROVAL.md"
CODE_VERSION = "graded-reversion-v1"

PHASE_A_SEEDS = tuple(range(100, 110))
PHASE_B_SEEDS = tuple(range(200, 210))
DRAW_SEEDS = PHASE_A_SEEDS + PHASE_B_SEEDS

# torch.Generator seed for direction j = 1..32. Disjoint from the training seeds.
DRAW_SEED_OFFSET = 40000
DRAW_SEED_STRIDE = 100

ALPHAS = (0.0, 0.125, 0.25, 0.5, 0.75, 1.0)
# Exact binary fractions: 1/16, 1/8, 3/16, 1/4, 1/4, 1/8.
AUC_WEIGHTS = (0.0625, 0.125, 0.1875, 0.25, 0.25, 0.125)
NORM_REL_TOL = 1e-12
SHOWN_MIN = 8
INVALID_MAX = 2
N_DOSES = 6
N_STEPS = 5

PRIMARY = "weight_hh"
TARGETS = (PRIMARY, "r", "z", "n")
PRIMARY_ROWS = (0, 24)

PHASE_A_DIR = "graded_reversion_phaseA_exploratory"
PHASE_B_DIR = "graded_reversion_results_v1"
PR7_CHECKPOINT_DIR = "recurrent_core_results_v1/checkpoints"
PR7_SEED_DIR = "recurrent_core_results_v1/seeds"

# Appendix A stays off. Phase B is gated by the approval note and by phase A.
APPENDIX_A_APPROVED = False

PHASE_A_PREFIX = (
    "EXPLORATORY (PHASE A, PR #7 SEEDS 100–109; DEVELOPMENT ONLY; NOT CONFIRMATORY)"
)
PHASE_A_HEADLINE = (
    "EXPLORATORY (PHASE A …; NOT CONFIRMATORY): per-seed curve results"
)

PRIMARY_REPLICATED = (
    "GRADED JOINT RECURRENT REVERSION EXCEEDS MATCHED RANDOM PERTURBATION "
    "(PREFIX FUNCTION): REPLICATED"
)
PRIMARY_NOT_MET = "GRADED JOINT REVERSION CRITERION NOT MET"
UNRESOLVED = "UNRESOLVED"
UNRESOLVED_E1 = "UNRESOLVED (E1 not replicated)"
SECONDARY_PREFIX = "Secondary (block-wise):"
E1_REPLICATED = "E1 REPLICATED"

CLAIM_SUCCESS = (
    "In W2, interpolation of the complete hidden-to-hidden matrix toward its "
    "initialization during updates 5–8, with trained input weights, biases and a "
    "fresh readout held fixed, increased oracle-referenced prefix-function loss "
    "over the predeclared dose grid. In at least eight of ten fresh seeds, the "
    "trapezoidal excess exceeded that of every one of 32 block-norm-matched "
    "random paths and reached at least one quarter of the paired prefix-loss "
    "advantage over F-INIT. The intact trained cores also outperformed the "
    "prefix-blind reference."
)
CLAIM_LIMITATION = (
    "This supports a bounded causal contribution of the trained hidden-to-hidden "
    "parameters to accurate prefix-dependent prediction under the specified "
    "intervention and fixed surrounding computation. It does not establish "
    "monotonicity, selectivity over continuation processing, localized content, "
    "necessity, or a uniquely identified mechanism."
)
CLAIM_NOT_MET = (
    "Graded joint recurrent reversion did not meet the prespecified curve-level "
    "criterion for prefix-function loss (%d/10 seeds passed; directional %d/10, "
    "materiality %d/10; eligibility failures %d/10)."
)
CLAIM_UNRESOLVED_E1 = (
    "Graded joint recurrent reversion was UNRESOLVED (E1 not replicated)."
)
CLAIM_UNRESOLVED_INVALID = (
    "Graded joint recurrent reversion was UNRESOLVED (more than two invalid seeds)."
)

D_RULE = "D passes iff AUC_REV − max_j AUC_rand,j > eps0."
SATURATION_RULE = (
    "Report Delta_REV(1/2) / Delta_REV(1) only when Delta_REV(1) > eps0; "
    "otherwise report UNDEFINED. Negative numerators remain signed. Do not apply "
    "the nonnegative E3 ratio convention to signed loss differences."
)
DENOMINATOR_RULE = (
    "At least eight of the ten prespecified phase-B seeds jointly satisfy "
    "validity, eligibility, D and M. The denominator remains ten; seeds are not "
    "removed from it."
)
ENDPOINT_SENTENCE = (
    "At alpha=1, only the hidden-to-hidden matrices during updates 5–8 equal "
    "their initialization. Input-to-hidden weights, biases, updates 1–4 and the "
    "fresh readout remain trained. This condition is not F-INIT, even apart from "
    "the readout difference."
)
READOUT_LIMITATION = (
    "Holding the same readout fixed in REV and random conditions controls readout "
    "identity, but does not eliminate differential disruption of compatibility "
    "among recurrent matrices, input weights, biases and the readout."
)
DISPLACEMENT_RULE = (
    "Primary eligibility requires ||delta||_F > eps0. A block with exactly zero "
    "displacement receives a zero random perturbation. Nonzero blocks are "
    "rescaled to their own displacement norm. Secondary eligibility requires "
    "||delta_k||_F > eps0 for the tested block."
)
AUC_DISCLAIMER = (
    "AUC is the integral of the piecewise-linear interpolant through the six "
    "measured dose-excess values. It is not a certified integral of the network's "
    "continuous dose response. Negative excesses are retained; no clipping or "
    "absolute-value transformation is applied."
)
UNDEFINED = "UNDEFINED"

TRANSFER_SHOWN = "TRANSFER SHOWN"
TRANSFER_NOT_SHOWN = "TRANSFER NOT SHOWN"

EDGE_LIMITED = "TUNED RIVAL STILL EDGE-LIMITED"
GRID_QUALIFIER = "within the declared 47-configuration grid"

CODE_FILES = (
    PROTOCOL_FILENAME,
    DEVIATIONS_FILENAME,
    APPROVAL_FILENAME,
    "graded_reversion_spec.py",
    "graded_reversion_draws.py",
    "graded_reversion_outcomes.py",
    "graded_reversion_eval.py",
    "graded_reversion_verdicts.py",
    "graded_reversion_train.py",
    "graded_reversion_appendix_a.py",
    "graded_reversion_report.py",
    "graded_reversion_study.py",
    "test_graded_reversion.py",
)

BANNED_PHASE_A_WORDS = ("REPLICATED", "DEMONSTRATED", "SHOWN", "CONFIRMED")


def draw_generator_seed(seed: int) -> int:
    return DRAW_SEED_OFFSET + DRAW_SEED_STRIDE * int(seed)


def target_rows(target: str) -> tuple[int, int]:
    if target == PRIMARY:
        return PRIMARY_ROWS
    if target not in GATE_ROWS:
        raise ValueError(target)
    return GATE_ROWS[target]
