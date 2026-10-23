"""Frozen constants for the two-stream acquisition study v1.

Every threshold, seed, split, budget, and arm below is taken from
TWOSTREAM_ACQUISITION_PROTOCOL_v1.md. Do not retune them after seeing
training output.
"""

from __future__ import annotations

from dataclasses import dataclass

PROTOCOL_SHA256 = "5fa5a795859d5ea7ee74f90fb043e143b484e32445741e9e4141a27d7dbf5d7c"

SEEDS = tuple(range(10))
STEPS = 4000
BATCH = 256
LR_INIT = 1e-3
LR_FINAL = 1e-4
GRAD_CLIP = 1.0
ADAM_BETA1 = 0.9
ADAM_BETA2 = 0.999
ADAM_EPS = 1e-8

# Prospective engineering criteria. Not theoretical significance thresholds.
A_FIT_FRACTION = 0.25
E2_RATIO = 0.5
E3_PARTIAL_MAX = 0.5
E3_WRONG_MAX = 0.5
E3_COMPLEMENT_MIN = 0.75
SIGMA_SEP = 0.1  # 1/10
XOR_CHANGE_MIN = 0.01  # 1/100
TAU_DEN = 0.01  # 1/100
NORM_MATCH = 0.20
COVERAGE_MIN = 0.10
MIN_DISTINCT = 4
RIDGE_LAMBDA = 1e-3
RANK_RELATIVE = 1e-8
RATIO_TIE = 1e-12
IDENTITY_TOL = 1e-9
CONSTANT_SPAN = 1e-12
CHART_R2_MIN = 0.9
GENERALIZATION_XOR_FRACTION = 0.5
GENERALIZATION_TRAIN_FACTOR = 4.0
SHOWN_MIN = 8
NOT_SHOWN_MAX = 2
B_GRID = (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24)
N_STAGES = 8
INPUT_SIZE = 9  # reading ±1 plus an 8-stage one-hot
READOUT_HIDDEN = 32

# Literal labels and verdict strings. Wording is the protocol's.
E1_SHOWN = "SHOWN"
E1_NOT_SHOWN = "NOT SHOWN"
E1_UNRESOLVED = "UNRESOLVED"
E2_SUPPORTED = "RECURRENT ADAPTATION SUPPORTED"
E2_FROZEN = "FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET"
E2_UNCLEAR = "READOUT-ONLY INSUFFICIENT, RECURRENT CONTRIBUTION UNCLEAR"
E2_UNRESOLVED = "UNRESOLVED"
E3_LOCALIZED = "LOCALIZED BY THE CHART-DECODER INTERVENTION"
E3_NOT_LOCALIZED = "NOT LOCALIZED BY THIS INTERVENTION"
E3_UNRESOLVED = "UNRESOLVED"
STUDY_ADMIT = "ADMIT"
STUDY_REJECT = "REJECT"
STUDY_UNRESOLVED = "UNRESOLVED"

LABEL_TWO_DIMENSIONAL = "Two-dimensional rival reproduces performance"
LABEL_FROZEN_READOUT = "Frozen-recurrence readout reproduces performance"
LABEL_GENERALIZATION_WEAK = "Held-out generalization weak"
LABEL_CHART_ACCESSIBLE = "Chart linearly accessible"

BASE_CLAIM = (
    "Within a supplied generic recurrent architecture with an external timing "
    "scaffold, gradient training on environment-supplied terminal outcomes "
    "acquired a history-dependent prediction function for X, Y and XOR in "
    "the frozen W2 world."
)
E2_FROZEN_APPEND = (
    "A frozen-recurrence control (K-FR: the same initialized network with only "
    "the readout trained, same episodes and budget) also met A-FIT at this "
    "budget. CAND's recurrent contribution is not established by this comparison."
)
E2_SUPPORTED_APPEND = (
    "…with a reliable contribution from recurrent adaptation relative to a "
    "frozen-recurrence readout."
)
E3_LOCALIZED_APPEND = (
    "…and a chart-decodable 3-d subspace of native state carries donor-specific "
    "forecast content under the prespecified partial intervention"
)
E3_QUALIFIER = (
    "observed in CAND but not in the matched frozen-recurrence control under "
    "this budget"
)
PERMITTED_JOINT = (
    "Training recurrent parameters improved prediction relative to K-FR, and a "
    "cross-fitted chart-decoder subspace redirected forecasts under the "
    "specified partial interventions."
)
REJECT_SENTENCE = (
    "Acquisition of the prediction function was not shown in this architecture, "
    "budget and split."
)

# Implementation readings of clauses the protocol does not fully specify.
# These do not change any threshold, seed, split, budget, arm, or claim wording.
DEVIATIONS = (
    "Cosine schedule: at step t = 0..3999, lr(t) = 1e-4 + (1e-3-1e-4)*(1+cos(pi*t/3999))/2, so step 0 is 1e-3 and step 3999 is 1e-4. Adam uses PyTorch defaults beta1=0.9, beta2=0.999, eps=1e-8, weight decay 0. Gradient clip is the global L2 norm, threshold 1.0, applied to trainable parameters.",
    "The loss minimized is the mean over the batch of the sum of the three squared terminal errors.",
    "Observed bit 0 is encoded as -1 and bit 1 as +1. The external timing scaffold is the length-8 one-hot with a 1 in position k-1 at stage k, concatenated after the scalar reading.",
    "Episodes are drawn from the generative model with an independent torch.Generator of float64 uniforms, seeded at 1000+s. A uniform is a positive event when it is strictly below the float64 value of the protocol probability (1/2, 1/5, 1/50, or 1/40). Each candidate uses 31 uniforms in a fixed layout. TEST histories are rejected and do not count toward the 1,024,000 episodes. CAND and K-FR of the same configuration and seed share this stream because they share the sampler seed and the same sampling code.",
    "K-FR recurrent parameters, including biases, are created under torch seed s and then requires_grad is set false. Adam is constructed on the readout parameters only. The readout initialization matches CAND.",
    "Nearest-posterior donor ties in total variation are broken by the lowest stage-4 prefix integer. The partial nearest-posterior transplant uses the cross-fitted chart projector of the recipient's parity fold.",
    "If any GRU-8 CAND seed fails the coverage rule or has cross-fit numerical rank below 3 on either parity fold, the E3 label is UNRESOLVED. The E3 qualifier is added only when K-FR's own label is NOT LOCALIZED BY THIS INTERVENTION. A K-FR seed that is UNRESOLVED is not counted as NOT LOCALIZED.",
    "Restoration re-inserts the recipient's own saved state after each of stages 5, 6, 7, and 8 and continues on that recipient's remaining readings. The forecast must match the recipient within 1e-9. Whole-state transplant is checked on every ordered pair of distinct 4-prefixes and every 4-bit continuation.",
    "K-TAB's state is a discrete history index, so the real-vector partial interventions, nearest-posterior geometry, PCA probe, and stage-8 ridge probe are not applicable. Whole-state identity of the index is tested. K-TAB logits stay float32 and are not quantized. Its initialization is the zero table, so a relative recurrent-weight change is undefined; the absolute logit change is reported instead.",
    "For K-2D and K-2D-MLP the chart subspace is not fitted. The whole 2-d state is the partial transplant and the complement transplant is the zero displacement. Those statistics are descriptive only. The initial state is 0.",
    "The stage-8 ridge probe uses the same centered ridge as the chart decoder, lambda 1e-3, fit on the 192 TRAIN histories. TEST R^2 uses the TEST-set mean as the total-sum baseline.",
    "The exploratory PCA subspace is the top 3 principal components of the 192 TRAIN stage-4 states, one state per TRAIN history with equal history weight.",
    "Random-direction and random-subspace probes draw, for each eligible trial in (a, b, u) order, one standard-normal direction and one standard-normal 3-column matrix from torch generator seed 7000+s. Displacements are scaled to the chart-subspace displacement norm. They are descriptive only.",
    "Section 6.5 absolute error is the per-query absolute deviation and the sum of those three absolute deviations. Normalized error divides each of those by the L2 norm of Delta-star, only when that norm is at least 1/100.",
    "K-PCO removes the XOR head, so the second linear map has 2 outputs (readout parameter count 354) and q_XOR is q_X + q_Y - 2 q_X q_Y. The three-term loss is unchanged.",
    "Quantizer endpoints are the float64 min and max, then cast to float32 and held. Constant coordinates use the float32 endpoints. After stage-8 quantization of K-EXACT, the chart is reconstructed from the three indices and repaired before the forecast, because the retained state is the indices only. Nominal ledger bits are d times b_sel; stage-wise, constant coordinates are charged 0 bits. Both are reported.",
    "A-FIT compares float64 learner excesses with the float64 rounding of the exact rational threshold, one quarter of the exact split-specific reference. E2's ratio criterion uses the total excess. The XOR ratio is reported and is not an additional gate. A seed satisfies a positive A-FIT count only when its errors are finite; integrity is gated separately where the protocol lists it separately.",
    "Outputs outside (0, 1), including non-finite values, are integrity failures. Training is one process with torch.set_num_threads(1) and deterministic algorithms enabled. No seed is replaced.",
)


@dataclass(frozen=True)
class Spec:
    arm: str
    cell: str
    hidden: int
    seed: int
    outputs: int
    freeze_recurrent: bool

    def file_stem(self) -> str:
        return f"{self.arm.lower().replace('-', '')}_{self.cell}{self.hidden}_s{self.seed}"

    def configuration(self) -> str:
        if self.arm == "K-TAB":
            return "K-TAB"
        if self.arm == "K-PCO":
            return "K-PCO"
        if self.arm == "K-2D":
            return "K-2D"
        if self.arm == "K-2D-MLP":
            return "K-2D-MLP"
        cell = "GRU" if self.cell == "gru" else "RNN"
        return f"{self.arm} {cell}-{self.hidden}"


def iter_specs():
    """The 120 runs: four candidate cells, K-FR for each, then four rivals."""
    cells = (("gru", 4), ("gru", 8), ("gru", 16), ("rnn", 8))
    for cell, hidden in cells:
        for arm, freeze in (("CAND", False), ("K-FR", True)):
            for seed in SEEDS:
                yield Spec(arm, cell, hidden, seed, 3, freeze)
    for seed in SEEDS:
        yield Spec("K-2D", "gru", 2, seed, 3, False)
        yield Spec("K-2D-MLP", "mlp", 2, seed, 3, False)
        yield Spec("K-TAB", "table", 0, seed, 3, False)
        yield Spec("K-PCO", "gru", 8, seed, 2, False)


def is_test_history(history: int) -> bool:
    """h is TEST iff ((h mod 16) + floor(h/16)) mod 4 = 0."""
    return ((history % 16) + (history // 16)) % 4 == 0


def cosine_lr(step: int, steps: int = STEPS) -> float:
    """Endpoint-inclusive cosine from LR_INIT at step 0 to LR_FINAL at the last step."""
    import math

    if steps <= 1:
        return LR_FINAL
    scale = 0.5 * (1.0 + math.cos(math.pi * step / (steps - 1)))
    return LR_FINAL + (LR_INIT - LR_FINAL) * scale
