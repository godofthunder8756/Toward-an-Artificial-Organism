"""GRU-8 cores and checkpoint bytes for the recurrent-core transfer study.

The cell is PyTorch nn.GRU(9, 8). Readouts are 8→32→3 or 8→70→3.
Hidden-to-hidden overrides touch one 8×8 block of weight_hh_l0 during
selected stages and then restore the trained weights.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os

import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import torch
from torch import nn

from recurrent_core_transfer_spec import GATE_ROWS, HIDDEN, INPUT_SIZE

REC_KEYS = (
    "rnn.weight_ih_l0",
    "rnn.weight_hh_l0",
    "rnn.bias_ih_l0",
    "rnn.bias_hh_l0",
)


class MatrixOverride:
    """Temporary replacement of one gate's hidden-to-hidden block."""

    def __init__(self, stages, rows, weight_block, bias_block=None):
        self.stages = frozenset(int(stage) for stage in stages)
        self.rows = rows
        self.weight_block = weight_block
        self.bias_block = bias_block

    def applies(self, stage_idx: int) -> bool:
        return stage_idx in self.stages


class CoreGRU(nn.Module):
    def __init__(self, readout_hidden: int):
        super().__init__()
        if readout_hidden < 1:
            raise ValueError(readout_hidden)
        self.readout_hidden = int(readout_hidden)
        self.hidden = HIDDEN
        self.cell = "gru"
        self.outputs = 3
        self.rnn = nn.GRU(INPUT_SIZE, HIDDEN, batch_first=True)
        self.readout_fc1 = nn.Linear(HIDDEN, self.readout_hidden)
        self.readout_fc2 = nn.Linear(self.readout_hidden, 3)
        self.override = None

    def recurrent_parameters(self):
        return list(self.rnn.parameters())

    def readout_parameters(self):
        return list(self.readout_fc1.parameters()) + list(self.readout_fc2.parameters())

    def initial_state(self, batch: int, dtype, device):
        return torch.zeros(batch, self.hidden, dtype=dtype, device=device)

    def readout(self, state):
        return torch.sigmoid(self.readout_fc2(torch.tanh(self.readout_fc1(state))))

    def _gru_step(self, state, bit, stage_idx: int):
        reading = (bit.to(dtype=state.dtype) * 2 - 1).unsqueeze(1)
        one = state.new_zeros(bit.shape[0], 8)
        one[:, stage_idx] = 1
        packed = torch.cat([reading, one], dim=1).unsqueeze(1)
        _out, hidden = self.rnn(packed, state.unsqueeze(0))
        return hidden.squeeze(0)

    def step(self, state, bit, stage_idx: int):
        override = self.override
        if override is None or not override.applies(stage_idx):
            return self._gru_step(state, bit, stage_idx)
        weight = self.rnn.weight_hh_l0
        bias = self.rnn.bias_hh_l0
        saved_w = weight.detach().clone()
        saved_b = bias.detach().clone()
        row0, row1 = override.rows
        block = override.weight_block.to(dtype=weight.dtype, device=weight.device)
        weight.data[row0:row1, :] = block
        if override.bias_block is not None:
            bias_block = override.bias_block.to(dtype=bias.dtype, device=bias.device)
            bias.data[row0:row1] = bias_block
        try:
            return self._gru_step(state, bit, stage_idx)
        finally:
            weight.data.copy_(saved_w)
            bias.data.copy_(saved_b)

    def forward(self, bits):
        batch, length = bits.shape
        reading = (bits * 2 - 1).unsqueeze(-1)
        eye = torch.eye(length, device=bits.device, dtype=bits.dtype).expand(batch, length, length)
        inputs = torch.cat([reading, eye], dim=-1)
        hidden0 = bits.new_zeros(1, batch, self.hidden)
        _out, hidden = self.rnn(inputs, hidden0)
        return self.readout(hidden.squeeze(0))


def parameter_counts(model: CoreGRU) -> dict:
    recurrent = sum(p.numel() for p in model.recurrent_parameters())
    readout = sum(p.numel() for p in model.readout_parameters())
    return {"recurrent": recurrent, "readout": readout, "total": recurrent + readout}


def snapshot_state(model: nn.Module) -> dict:
    return {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}


def build_initialized(seed: int, readout_hidden: int) -> CoreGRU:
    torch.manual_seed(seed)
    return CoreGRU(readout_hidden)


def copy_recurrent(model: CoreGRU, state: dict) -> None:
    current = model.state_dict()
    for key in REC_KEYS:
        current[key] = state[key].detach().cpu().to(dtype=current[key].dtype).clone()
    model.load_state_dict(current)


def load_snapshot(model: CoreGRU, state: dict) -> None:
    payload = {
        key: value.detach().cpu().to(dtype=model.state_dict()[key].dtype).clone()
        for key, value in state.items()
    }
    model.load_state_dict(payload)


def tune_recurrent(state: dict, g: float, b: float) -> dict:
    """Scale weight_hh by g and add b to the update-gate bias. W^0 is not mutated."""
    tuned = {key: value.detach().cpu().clone() for key, value in state.items() if key in REC_KEYS}
    tuned["rnn.weight_hh_l0"] = tuned["rnn.weight_hh_l0"] * float(g)
    bias = tuned["rnn.bias_hh_l0"].clone()
    bias[8:16] = bias[8:16] + float(b)
    tuned["rnn.bias_hh_l0"] = bias
    return tuned


def eval_copy(model: CoreGRU) -> CoreGRU:
    cpu_state = torch.get_rng_state()
    try:
        copied = CoreGRU(model.readout_hidden).double().eval()
        payload = {key: value.detach().cpu().double() for key, value in model.state_dict().items()}
        copied.load_state_dict(payload)
        for parameter in copied.parameters():
            parameter.requires_grad_(False)
        copied.override = None
        return copied
    finally:
        torch.set_rng_state(cpu_state)


def canonical_payload(state: dict) -> dict:
    payload = {}
    for key in sorted(state):
        array = state[key].detach().cpu().contiguous().numpy()
        payload[key] = {
            "dtype": array.dtype.str,
            "shape": list(array.shape),
            "data_b64": base64.b64encode(array.tobytes()).decode("ascii"),
        }
    return payload


def canonical_bytes(state: dict) -> bytes:
    return json.dumps(canonical_payload(state), indent=2, sort_keys=True).encode("utf-8") + b"\n"


def checkpoint_sha256(state: dict) -> str:
    return hashlib.sha256(canonical_bytes(state)).hexdigest()


def save_checkpoint(path, state: dict) -> str:
    raw = canonical_bytes(state)
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def load_checkpoint(path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    state = {}
    for key, record in payload.items():
        raw = base64.b64decode(record["data_b64"])
        array = np.frombuffer(raw, dtype=np.dtype(record["dtype"])).reshape(record["shape"]).copy()
        state[key] = torch.from_numpy(array)
    return state


def gate_block(weight_hh: torch.Tensor, gate: str) -> torch.Tensor:
    row0, row1 = GATE_ROWS[gate]
    return weight_hh[row0:row1, :].detach().clone()
