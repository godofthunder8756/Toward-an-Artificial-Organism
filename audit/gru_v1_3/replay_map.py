"""Frozen source-field map for spec v1.3 §6. Declared before execution.

PR #8 and PR #9 map "intact" to f_trained. Fields marked unavailable here are
SOURCE-REPLAY UNAVAILABLE. That declaration is part of the freeze.
"""

# Protocol order of the PR #7 selection grid. Index i is this enumeration.
GRID_G = (0.5, 1.0, 2.0)
GRID_B = (-2.0, 0.0, 2.0)
GRID_GB = tuple((g, b) for g in GRID_G for b in GRID_B)

PR7_ERROR_ARMS = {
    "cand_final": "cand.errors",
    "cand_init": "cand.init_errors",
    "f_init": "f_init.errors",
    "f_trained": "f_trained.errors",
    "f_tuned32": "f_tuned32.errors",
    "r_tuned843": "r_tuned843.errors",
}

# Keys compared inside each errors object. Absolute tolerance 1e-12.
ERROR_KEYS = tuple(
    "%s.%s" % (split, name)
    for split in ("TRAIN", "TEST")
    for name in ("X", "Y", "XOR", "total")
)

PR10_E_FIELDS = (
    "L_prefix",
    "PD",
    "E_TEST.X",
    "E_TEST.Y",
    "E_TEST.XOR",
    "E_TEST.total",
    "E_TRAIN.X",
    "E_TRAIN.Y",
    "E_TRAIN.XOR",
    "E_TRAIN.total",
    "components.prefix",
    "components.total",
    "components.xor",
    "T",
)

REPLAY_MAP = {
    "tolerance_source_replay_absolute": 1e-12,
    "tolerance_numpy_vs_torch_max_abs": 1e-10,
    "tolerance_identity": "abs(a-b) <= 1e-12 + 1e-12*max(abs(a), abs(b))",
    "identity_extension_F4": "The same combined tolerance is applied to the e_P known-coefficient reconstruction.",
    "torch_reference": (
        "Decoder states and outputs are the float64 CoreGRU.step rollout used by "
        "evaluate_arm. CoreGRU.forward (one batched rnn call) is checked as well. "
        "Both must agree with the independent numpy float64 GRU to max-abs 1e-10."
    ),
    "zero_variance_rule": (
        "One rule everywhere: weighted population variance <= 1e-24 "
        "(equivalent to sd <= 1e-12). Used for §5 feature exclusion, §9 target "
        "variance, and descriptive correlations. Manifest note n1."
    ),
    "uniform_weight_r2": (
        "The uniform-weight sensitivity uses full-domain uniform-weight Var(q) "
        "as the R^2 denominator and receives no meets-floor, below-floor, or "
        "BOUNDARY label. Manifest note n2."
    ),
    "pr7": {
        "record": "recurrent_core_results_v1/seeds/s{seed}.json",
        "commit_ref": "origin/pr/7",
        "route_errors": "evaluate_arm: eval_copy, rollout via CoreGRU.step, component_excess",
        "route_selection": "predict_histories on VAL histories, then probability_excess total",
        "error_arms": PR7_ERROR_ARMS,
        "error_keys": ERROR_KEYS,
        "selection": {
            "field": "selection.grid[i].criterion",
            "index_order": "GRID_G × GRID_B = (0.5, 1.0, 2.0) × (-2.0, 0.0, 2.0)",
            "arm_pattern": "sel_g{g}_b{b}",
        },
    },
    "pr8": {
        "record": "graded_reversion_results_v1/seeds/s{seed}.json",
        "commit_ref": "origin/pr/8",
        "intact_maps_to": "f_trained",
        "route": "module_from_state -> eval_copy -> rollout -> component_excess",
        "available": {
            "f_trained": "evaluation.intact_outcomes.E_{TEST,TRAIN}_{X,Y,XOR,total}",
            "f_init": "evaluation.f_init_outcomes.E_{TEST,TRAIN}_{X,Y,XOR,total}",
        },
        "unavailable": {
            "cand_final": "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED",
            "cand_init": "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED",
        },
    },
    "pr9": {
        "record": "first_order_control_results_v1/seeds/s{seed}.json",
        "commit_ref": "origin/pr/9",
        "intact_maps_to": "f_trained",
        "route": "module_from_state -> eval_copy -> rollout -> component_excess",
        "available": {
            "f_trained": "evaluation.intact_outcomes.E_{TEST,TRAIN}_{X,Y,XOR,total}",
            "f_init": "evaluation.f_init_outcomes.E_{TEST,TRAIN}_{X,Y,XOR,total}",
        },
        "unavailable": {
            "cand_final": "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED",
            "cand_init": "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED",
        },
    },
    "pr10": {
        "record": "frozen_recurrent_compensation_results_v1/stage2/results.json",
        "commit_ref": "origin/pr/10",
        "match": "runs[*] matched by seed and arm",
        "init_side": "init",
        "trained_side": "final",
        "init_checkpoints": "frozen_recurrent_compensation_results_v1/stage0/checkpoints",
        "trained_checkpoints": "frozen_recurrent_compensation_results_v1/stage1/checkpoints",
        "fields": PR10_E_FIELDS,
        "blocks": ("E1", "E2"),
        "route_E1": "torch float64 evaluate_arm predictions, l_prefix, component_excess, normalized components",
        "route_E2": "independent numpy float64 forward and the same metric formulas",
        "arms": ("CAND", "R-FIX-32", "R-FIX-48"),
    },
    "source_replay_unavailable_label": (
        "SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED means source-metric replay "
        "is unavailable but tier (i) hash/load and tier (iii) numpy-versus-torch "
        "forward agreement passed. It does not certify agreement with an unavailable "
        "historical metric."
    ),
}


def selection_index(arm):
    """Return i for sel_g*_b* under the frozen grid order, or None."""
    for i, (g, b) in enumerate(GRID_GB):
        name = "sel_g%s_b%s" % (_num(g), _num(b))
        if arm == name:
            return i
    return None


def _num(value):
    text = "%s" % value
    if text.endswith(".0"):
        return text
    return text
