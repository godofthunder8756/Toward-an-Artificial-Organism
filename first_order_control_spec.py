"""Frozen constants for graded reversion against FO and ISO controls.

Scientific values are the FINAL protocol's. Nothing here is retuned after a
phase A or phase B curve is seen. Readings of underspecified mechanics are
listed in first_order_control_DEVIATIONS_AND_AMBIGUITIES.md.
"""

from __future__ import annotations

from graded_reversion_spec import (
    ALPHAS,
    AUC_DISCLAIMER,
    AUC_WEIGHTS,
    DISPLACEMENT_RULE,
    ENDPOINT_SENTENCE,
    EPS0,
    IDENTITY_TOL,
    N_RANDOM,
    PRIMARY,
    READOUT_LIMITATION,
    SATURATION_RULE,
    TARGETS,
)

PROTOCOL_FILENAME = "first_order_control_protocol_FINAL.md"
PROTOCOL_SHA256 = "0efce40bdf2cf55af61f8c70f817ec3fbf8fe3a79256025556a77a03f8347101"
DEVIATIONS_FILENAME = "first_order_control_DEVIATIONS_AND_AMBIGUITIES.md"
FREEZE_FILENAME = "FIRST_ORDER_CONTROL_FREEZE_v1.json"
APPROVAL_FILENAME = "FIRST_ORDER_CONTROL_PHASE_B_APPROVAL.md"
CODE_VERSION = "first-order-control-v1"

PHASE_A_SEEDS = tuple(range(100, 110)) + tuple(range(200, 210))
PHASE_A_PR7_SEEDS = tuple(range(100, 110))
PHASE_A_PR8_SEEDS = tuple(range(200, 210))
PHASE_B_SEEDS = tuple(range(300, 310))
MANIFEST_SEEDS = PHASE_A_SEEDS + PHASE_B_SEEDS

# ISO reuses the PR #8 generator: 40000 + 100*s. Seeds 300-309 are 70000-70900.
FO_SEED_OFFSET = 1_000_000
FO_SEED_STRIDE = 100
GRAD_SEED_OFFSET = 2_000_000
GRAD_SEED_STRIDE = 100
N_PATHS = N_RANDOM
N_GRAD_RANDOM = 3
BLOCKS = ("r", "z", "n")

NORM_REL_TOL = 1e-12
FO_REL_TOL = 1e-12
ORTH_TOL = 1e-12
RADIUS_REL_TOL = 1e-12
FD_ABS_FLOOR = 1e-10
FD_REL = 1e-6
FD_STEP = 1e-6
G_ZERO = 1e-10
RHO_COLLAPSE = 1e-3
RHO_NEAR = 0.10
PROJECTION_FAIL_REL = 1e-12
THIN_REL = 0.10
SHOWN_MIN = 8
UNEVALUABLE_MAX = 2
CROSS_CHECK_ABS = 1e-15
TIED_GRAD_ATOL = 1e-18
N_DOSES = 6

PHASE_A_DIR = "first_order_control_phaseA_exploratory"
PHASE_B_DIR = "first_order_control_results_v1"
PR7_CHECKPOINT_DIR = "recurrent_core_results_v1/checkpoints"
PR8_CHECKPOINT_DIR = "graded_reversion_results_v1/checkpoints"
PR8_FREEZE_FILENAME = "GRADED_REVERSION_FREEZE_v1.json"

PHASE_A_PREFIX = (
    "EXPLORATORY (PHASE A, PR #7 SEEDS 100–109 / PR #8 SEEDS 200–209; "
    "DEVELOPMENT ONLY; NOT CONFIRMATORY)"
)
PHASE_A_HEADLINE = (
    "EXPLORATORY (PHASE A …; NOT CONFIRMATORY): per-seed curve results"
)

PRIMARY_REPLICATED = (
    "GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC "
    "CONTROLS (PREFIX FUNCTION): REPLICATED"
)
PRIMARY_NOT_MET = "JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET"
UNRESOLVED_E1 = "UNRESOLVED (E1 not replicated)"
UNRESOLVED_INSUFFICIENT = "UNRESOLVED (insufficient evaluable seeds)"
SECONDARY_PREFIX = "Secondary (block-wise), %s:"

CLAIM_SUCCESS = (
    "In W2, in at least eight of ten fresh GRU-8 seeds, continuation-stage "
    "joint recurrent reversion produced a trapezoidal excess prefix-function "
    "loss exceeding every one of 32 first-order-matched paths and every one of "
    "32 isotropic paths. Both families matched the reversion displacement block "
    "by block in Frobenius norm; the first-order-matched family additionally "
    "matched its initial loss derivative. The excess met the declared "
    "materiality threshold, and the intact trained cores outperformed the "
    "prefix-blind reference. This supports a bounded causal contribution under "
    "the specified intervention and fixed surrounding computation. The "
    "comparison concerns the sampled families and dose-averaged AUC; it does "
    "not identify semantic content, curvature as a mechanism, localization, "
    "necessity, or selectivity over continuation processing."
)
CLAIM_NOT_MET = (
    "The joint FO-and-ISO criterion was not met; no reduction was identified."
)
CLAIM_UNRESOLVED_E1 = (
    "Graded joint reversion against first-order-matched and isotropic controls "
    "was UNRESOLVED (E1 not replicated)."
)
CLAIM_UNRESOLVED_INSUFFICIENT = (
    "Graded joint reversion against first-order-matched and isotropic controls "
    "was UNRESOLVED (insufficient evaluable seeds)."
)
DISCLOSURE = (
    "The first-order matching uses the gradient of the oracle-referenced "
    "prefix-function loss at the trained weights. It is an oracle-informed "
    "analysis control, applied after training; it is not network training and "
    "does not train the network or modify its saved checkpoint."
)
SINGLE_BLOCK_SENTENCE = (
    "The primary effect was not reproduced by any single block at the declared "
    "criterion."
)
ROBUSTNESS_SENTENCE = (
    "The REPLICATED label depends on at least one seed whose directional margin "
    "against at least one family is below 10% of that family's most damaging "
    "sampled path; robustness to additional draws is untested."
)
RESIDUAL_NAME = "residual after subtracting the initial tangent contribution"
NOT_CURVATURE = "It is not a curvature estimate."
MONOTONIC_NOTE = (
    "Sampled non-decreasing values do not imply a continuously monotonic path."
)
UNDEFINED = "UNDEFINED"
FAMILY_FO = "first-order-matched"
FAMILY_ISO = "isotropic"

D_RULE = (
    "D_FO = (AUC_REV - max_j AUC_FO,j > eps0); "
    "D_ISO = (AUC_REV - max_j AUC_ISO,j > eps0); "
    "D = D_FO and D_ISO; "
    "Joint pass = valid and eligible and D_FO and D_ISO and M."
)

CODE_FILES = (
    PROTOCOL_FILENAME,
    DEVIATIONS_FILENAME,
    APPROVAL_FILENAME,
    "first_order_control_spec.py",
    "first_order_control_draws.py",
    "first_order_control_construct.py",
    "first_order_control_gradient.py",
    "first_order_control_criteria.py",
    "first_order_control_verdicts.py",
    "first_order_control_eval.py",
    "first_order_control_train.py",
    "first_order_control_report.py",
    "first_order_control_study.py",
    "test_first_order_control.py",
)

BANNED_PHASE_A_WORDS = ("REPLICATED", "DEMONSTRATED", "SHOWN", "CONFIRMED")

# Inherited strings re-exported so reports can quote them without editing PR #8.
INHERITED_AUC_DISCLAIMER = AUC_DISCLAIMER
INHERITED_ENDPOINT_SENTENCE = ENDPOINT_SENTENCE
INHERITED_READOUT_LIMITATION = READOUT_LIMITATION
INHERITED_SATURATION_RULE = SATURATION_RULE
INHERITED_DISPLACEMENT_RULE = DISPLACEMENT_RULE
INHERITED_ALPHAS = ALPHAS
INHERITED_AUC_WEIGHTS = AUC_WEIGHTS
INHERITED_EPS0 = EPS0
INHERITED_IDENTITY_TOL = IDENTITY_TOL
INHERITED_PRIMARY = PRIMARY
INHERITED_TARGETS = TARGETS


def fo_generator_seed(seed: int) -> int:
    return FO_SEED_OFFSET + FO_SEED_STRIDE * int(seed)


def grad_generator_seed(seed: int) -> int:
    return GRAD_SEED_OFFSET + GRAD_SEED_STRIDE * int(seed)
