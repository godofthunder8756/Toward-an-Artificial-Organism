"""Float64 GRU-8 forwards.

The numpy forward is independent of torch. The torch paths reproduce
CoreGRU.step (evaluate_arm / rollout) and CoreGRU.forward (one batched rnn call).
Weights are float64 casts of the stored float32 parameters.
"""

from __future__ import annotations

import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.set_num_interop_threads(1)


def sigmoid(values: np.ndarray) -> np.ndarray:
    out = np.empty(values.shape, dtype=np.float64)
    positive = values >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-values[positive]))
    exponential = np.exp(values[~positive])
    out[~positive] = exponential / (1.0 + exponential)
    return out


def numpy_forward(weights: dict, bits: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return stage-8 state (n, 8) and sigmoid readout (n, 3)."""
    state = np.zeros((bits.shape[0], 8), dtype=np.float64)
    for stage in range(bits.shape[1]):
        packed = np.zeros((bits.shape[0], 9), dtype=np.float64)
        packed[:, 0] = bits[:, stage] * 2.0 - 1.0
        packed[:, stage + 1] = 1.0
        gates_i = packed @ weights["w_ih"].T + weights["b_ih"]
        gates_h = state @ weights["w_hh"].T + weights["b_hh"]
        i_r, i_z, i_n = np.split(gates_i, 3, axis=1)
        h_r, h_z, h_n = np.split(gates_h, 3, axis=1)
        reset = sigmoid(i_r + h_r)
        update = sigmoid(i_z + h_z)
        new = np.tanh(i_n + reset * h_n)
        state = (1.0 - update) * new + update * state
    hidden = np.tanh(state @ weights["w1"].T + weights["b1"])
    output = sigmoid(hidden @ weights["w2"].T + weights["b2"])
    return state, output


def _as_f64(array: np.ndarray) -> np.ndarray:
    return np.array(array, dtype=np.float64, copy=True)


def weights_from_checkpoint(payload: dict) -> dict:
    def take(key):
        record = payload[key]
        raw = __import__("base64").b64decode(record["data_b64"])
        array = np.frombuffer(raw, dtype=np.dtype(record["dtype"])).reshape(record["shape"]).copy()
        return _as_f64(array)

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


def _torch_modules(weights: dict):
    hidden_out = weights["w1"].shape[0]
    rnn = nn.GRU(9, 8, batch_first=True).double()
    fc1 = nn.Linear(8, hidden_out).double()
    fc2 = nn.Linear(hidden_out, 3).double()
    with torch.no_grad():
        rnn.weight_ih_l0.copy_(torch.from_numpy(weights["w_ih"]))
        rnn.weight_hh_l0.copy_(torch.from_numpy(weights["w_hh"]))
        rnn.bias_ih_l0.copy_(torch.from_numpy(weights["b_ih"]))
        rnn.bias_hh_l0.copy_(torch.from_numpy(weights["b_hh"]))
        fc1.weight.copy_(torch.from_numpy(weights["w1"]))
        fc1.bias.copy_(torch.from_numpy(weights["b1"]))
        fc2.weight.copy_(torch.from_numpy(weights["w2"]))
        fc2.bias.copy_(torch.from_numpy(weights["b2"]))
    rnn.eval()
    fc1.eval()
    fc2.eval()
    return rnn, fc1, fc2


def _readout(fc1, fc2, state: torch.Tensor) -> torch.Tensor:
    return torch.sigmoid(fc2(torch.tanh(fc1(state))))


def torch_step_forward(weights: dict, bits: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """CoreGRU.step / rollout path. Returns state and output as float64 arrays."""
    rnn, fc1, fc2 = _torch_modules(weights)
    bits_t = torch.from_numpy(np.ascontiguousarray(bits, dtype=np.float64))
    batch = bits_t.shape[0]
    with torch.inference_mode():
        state = torch.zeros(batch, 8, dtype=torch.float64)
        for stage in range(bits_t.shape[1]):
            reading = (bits_t[:, stage] * 2 - 1).unsqueeze(1)
            one = torch.zeros(batch, 8, dtype=torch.float64)
            one[:, stage] = 1
            packed = torch.cat([reading, one], dim=1).unsqueeze(1)
            _out, hidden = rnn(packed, state.unsqueeze(0))
            state = hidden.squeeze(0)
        output = _readout(fc1, fc2, state)
    return state.detach().cpu().numpy().copy(), output.detach().cpu().numpy().copy()


def torch_batched_forward(weights: dict, bits: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """CoreGRU.forward path: one batched rnn call over the eight stages."""
    rnn, fc1, fc2 = _torch_modules(weights)
    bits_t = torch.from_numpy(np.ascontiguousarray(bits, dtype=np.float64))
    batch, length = bits_t.shape
    with torch.inference_mode():
        reading = (bits_t * 2 - 1).unsqueeze(-1)
        eye = torch.eye(length, dtype=torch.float64).expand(batch, length, length)
        inputs = torch.cat([reading, eye], dim=-1)
        hidden0 = torch.zeros(1, batch, 8, dtype=torch.float64)
        _out, hidden = rnn(inputs, hidden0)
        state = hidden.squeeze(0)
        output = _readout(fc1, fc2, state)
    return state.detach().cpu().numpy().copy(), output.detach().cpu().numpy().copy()
