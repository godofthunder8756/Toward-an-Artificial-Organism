"""Dual evaluation. E1 is the frozen evaluator. E2 is the NumPy forward pass.

Float32 output is descriptive and does not gate. No consciousness claim.
"""

from __future__ import annotations

import numpy as np
import torch

from graded_reversion_outcomes import l_prefix, pd_cd_components
from recurrent_core_transfer_metrics import evaluate_arm
from recurrent_core_transfer_models import CoreGRU, load_snapshot
from twostream_acquisition_metrics import all_bits, component_excess, outputs_valid

from frozen_recurrent_compensation_numpy_eval import evaluate as numpy_evaluate
from frozen_recurrent_compensation_spec import (
    COMPONENT_NAMES,
    INTEGRITY,
    classify_T,
    components_agree,
    values_agree,
)


def arrays_from_state(state: dict) -> dict:
    def take(key):
        tensor = state[key]
        if hasattr(tensor, "detach"):
            tensor = tensor.detach().cpu().contiguous().numpy()
        return np.array(tensor, dtype=np.float64, copy=True)

    return {
        "w_ih": take("rnn.weight_ih_l0"),
        "w_hh": take("rnn.weight_hh_l0"),
        "b_ih": take("rnn.bias_ih_l0"),
        "b_hh": take("rnn.bias_hh_l0"),
        "w1": take("readout_fc1.weight"),
        "b1": take("readout_fc1.bias"),
        "w2": take("readout_fc2.weight"),
        "b2": take("readout_fc2.bias"),
    }


def _pack(prefix: float, errors: dict, pd: float, thr_total: float, thr_xor: float) -> dict:
    from frozen_recurrent_compensation_numpy_eval import normalized_components

    components = normalized_components(
        prefix,
        errors["TEST"]["total"],
        errors["TEST"]["XOR"],
        pd,
        thr_total,
        thr_xor,
    )
    return {
        "L_prefix": float(prefix),
        "PD": float(pd),
        "E_TEST": {key: float(errors["TEST"][key]) for key in ("X", "Y", "XOR", "total")},
        "E_TRAIN": {key: float(errors["TRAIN"][key]) for key in ("X", "Y", "XOR", "total")},
        "components": components,
        "components_repr": {name: repr(components[name]) for name in COMPONENT_NAMES},
        "T": float(max(components[name] for name in COMPONENT_NAMES)),
        "T_repr": repr(float(max(components[name] for name in COMPONENT_NAMES))),
    }


def binding_names(components: dict | None) -> list[str] | None:
    if components is None:
        return None
    best = max(components[name] for name in COMPONENT_NAMES)
    return [name for name in COMPONENT_NAMES if components[name] == best]


def _float32_predictions(model) -> np.ndarray:
    was_training = model.training
    model.eval()
    bits = torch.from_numpy(np.ascontiguousarray(all_bits(), dtype=np.float32))
    with torch.inference_mode():
        predictions = model(bits).detach().cpu().numpy().astype(np.float64, copy=False)
    model.train(was_training)
    return predictions


def evaluate_state(state: dict, readout_hidden: int, world, thr_total: float, thr_xor: float, val_mask: np.ndarray) -> dict:
    """E1 and E2 on one float32 state. Does not train."""
    model = CoreGRU(readout_hidden)
    load_snapshot(model, state)
    arm = evaluate_arm(model, world)
    predictions = arm["predictions"]
    explicit = component_excess(predictions, world)
    for split in ("TEST", "TRAIN"):
        for key in ("X", "Y", "XOR", "total"):
            if explicit[split][key] != arm["errors"][split][key]:
                raise RuntimeError("component_excess disagreed with evaluate_arm")
    pd = pd_cd_components(world.q)["PD"]
    e1 = _pack(l_prefix(predictions, world.q), explicit, pd, thr_total, thr_xor)
    e2_raw = numpy_evaluate(
        arrays_from_state(state),
        world.q,
        world.probability,
        world.is_test,
        thr_total,
        thr_xor,
        val_mask,
    )
    e2 = {
        "L_prefix": e2_raw["L_prefix"],
        "PD": e2_raw["PD"],
        "E_TEST": e2_raw["E_TEST"],
        "E_TRAIN": e2_raw["E_TRAIN"],
        "components": e2_raw["components"],
        "components_repr": {name: repr(e2_raw["components"][name]) for name in COMPONENT_NAMES},
        "T": e2_raw["T"],
        "T_repr": repr(e2_raw["T"]),
    }
    agreed = components_agree(e1["components"], e2["components"])
    numeric = classify_T(e1["T"], e2["T"], agreed)
    if agreed and numeric == INTEGRITY:
        raise RuntimeError("classifier returned integrity after agreement")
    float32_preds = _float32_predictions(model)
    float32_errors = component_excess(float32_preds, world)
    float32 = _pack(l_prefix(float32_preds, world.q), float32_errors, pd, thr_total, thr_xor)
    from recurrent_core_transfer_metrics import probability_excess

    histories = [index for index in range(256) if bool(val_mask[index])]
    selected = predictions[np.asarray(histories, dtype=np.int64)]
    val_e1 = probability_excess(selected, histories, world)
    identity = arm["identity"]
    e1_valid = bool(outputs_valid(predictions)) and bool(arm["outputs_valid"])
    return {
        "evaluated": True,
        "E1": e1,
        "E2": e2,
        "float32_descriptive": float32,
        "components_agree": bool(agreed),
        "agreement_gaps": {
            name: abs(e1["components"][name] - e2["components"][name]) for name in COMPONENT_NAMES
        },
        "prediction_max_abs": float(np.max(np.abs(predictions - e2_raw["predictions"]))),
        "numeric_class": numeric,
        "binding_E1": binding_names(e1["components"]),
        "binding_E2": binding_names(e2["components"]),
        "outputs_valid_E1": e1_valid,
        "outputs_valid_E2": bool(e2_raw["outputs_valid"]),
        "identity_ok": bool(identity["ok"]),
        "identity": {
            "whole_state_ok": bool(identity["whole_state_ok"]),
            "restoration_ok": bool(identity["restoration_ok"]),
            "ok": bool(identity["ok"]),
        },
        "val_E1": val_e1,
        "val_E2": e2_raw["val"],
        "values_agree_T": values_agree(e1["T"], e2["T"]),
    }


def evaluation_reasons(block: dict) -> list[str]:
    reasons = []
    if not block["outputs_valid_E1"] or not block["outputs_valid_E2"]:
        reasons.append("outputs_valid")
    if not block["identity_ok"]:
        reasons.append("identity")
    if not block["components_agree"]:
        reasons.append("evaluator_disagreement")
    return reasons
