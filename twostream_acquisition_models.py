"""Candidate and rival networks for the acquisition study.

Parameter counts follow PyTorch's default initializers and biases. Recurrent
cells are nn.GRU or nn.RNN (tanh). The K-2D-MLP cell is the declared
two-layer tanh update. K-TAB is a table of 256 x 3 logits.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import torch
from torch import nn

from twostream_acquisition_spec import INPUT_SIZE, READOUT_HIDDEN, Spec


class VectorArm(nn.Module):
    """Recurrent arm with an MLP readout. outputs=2 selects the product XOR head."""

    def __init__(self, cell: str, hidden: int, outputs: int = 3):
        super().__init__()
        if cell not in ("gru", "rnn", "mlp"):
            raise ValueError(cell)
        if hidden < 1:
            raise ValueError(hidden)
        self.cell = cell
        self.hidden = hidden
        self.outputs = outputs
        self.product_xor = outputs == 2
        if cell == "gru":
            self.rnn = nn.GRU(INPUT_SIZE, hidden, batch_first=True)
        elif cell == "rnn":
            self.rnn = nn.RNN(INPUT_SIZE, hidden, nonlinearity="tanh", batch_first=True)
        else:
            self.update_a = nn.Linear(hidden + 1 + 8, 16)
            self.update_b = nn.Linear(16, hidden)
        self.readout_fc1 = nn.Linear(hidden, READOUT_HIDDEN)
        self.readout_fc2 = nn.Linear(READOUT_HIDDEN, outputs)

    def recurrent_parameters(self):
        if self.cell == "mlp":
            return list(self.update_a.parameters()) + list(self.update_b.parameters())
        return list(self.rnn.parameters())

    def readout_parameters(self):
        return list(self.readout_fc1.parameters()) + list(self.readout_fc2.parameters())

    def initial_state(self, batch: int, dtype, device):
        return torch.zeros(batch, self.hidden, dtype=dtype, device=device)

    def step(self, state, bit, stage_idx: int):
        reading = (bit.to(dtype=state.dtype) * 2 - 1).unsqueeze(1)
        one = state.new_zeros(bit.shape[0], 8)
        one[:, stage_idx] = 1
        if self.cell == "mlp":
            packed = torch.cat([state, reading, one], dim=1)
            return torch.tanh(self.update_b(torch.tanh(self.update_a(packed))))
        packed = torch.cat([reading, one], dim=1).unsqueeze(1)
        _out, hidden = self.rnn(packed, state.unsqueeze(0))
        return hidden.squeeze(0)

    def readout(self, state):
        raw = torch.sigmoid(self.readout_fc2(torch.tanh(self.readout_fc1(state))))
        if not self.product_xor:
            return raw
        qx = raw[:, 0]
        qy = raw[:, 1]
        qxor = qx + qy - 2 * qx * qy
        return torch.stack([qx, qy, qxor], dim=1)

    def forward(self, bits):
        """Training forward. bits is (batch, 8) with entries in {0, 1}."""
        batch, length = bits.shape
        if self.cell == "mlp":
            state = bits.new_zeros(batch, self.hidden)
            for stage in range(length):
                state = self.step(state, bits[:, stage], stage)
            return self.readout(state)
        reading = (bits * 2 - 1).unsqueeze(-1)
        eye = torch.eye(length, device=bits.device, dtype=bits.dtype).expand(batch, length, length)
        inputs = torch.cat([reading, eye], dim=-1)
        hidden0 = bits.new_zeros(1, batch, self.hidden)
        _out, hidden = self.rnn(inputs, hidden0)
        return self.readout(hidden.squeeze(0))


class TableArm(nn.Module):
    """History table. The state is the integer of bits seen so far."""

    def __init__(self):
        super().__init__()
        self.cell = "table"
        self.hidden = 0
        self.outputs = 3
        self.product_xor = False
        self.logits = nn.Parameter(torch.zeros(256, 3))

    def recurrent_parameters(self):
        return []

    def readout_parameters(self):
        return [self.logits]

    def initial_state(self, batch: int, dtype, device):
        return torch.zeros(batch, dtype=torch.long, device=device)

    def step(self, state, bit, stage_idx: int):
        return state | (bit.to(dtype=torch.long) << stage_idx)

    def readout(self, state):
        return torch.sigmoid(self.logits[state])

    def forward(self, bits):
        powers = (2 ** torch.arange(bits.shape[1], device=bits.device)).to(torch.long)
        index = (bits.to(torch.long) * powers).sum(dim=1)
        return torch.sigmoid(self.logits[index])


def build_model(spec: Spec) -> nn.Module:
    if spec.cell == "table":
        return TableArm()
    return VectorArm(spec.cell, spec.hidden, spec.outputs)


def parameter_counts(model: nn.Module) -> dict:
    recurrent = sum(p.numel() for p in model.recurrent_parameters())
    readout = sum(p.numel() for p in model.readout_parameters())
    return {"recurrent": recurrent, "readout": readout, "total": recurrent + readout}


def snapshot_state(model: nn.Module) -> dict:
    return {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}


def load_snapshot(model: nn.Module, state: dict) -> None:
    model.load_state_dict(state)


def eval_copy(model: nn.Module) -> nn.Module:
    """Float64 evaluation copy. Training weights stay float32.

    Construction draws the global generator and then overwrites every weight,
    so the generator state is restored.
    """
    cpu_state = torch.get_rng_state()
    try:
        copied = build_model(_spec_of(model)).double().eval()
        payload = {key: value.detach().cpu().double() for key, value in model.state_dict().items()}
        copied.load_state_dict(payload)
        for parameter in copied.parameters():
            parameter.requires_grad_(False)
        return copied
    finally:
        torch.set_rng_state(cpu_state)


def _spec_of(model: nn.Module) -> Spec:
    if isinstance(model, TableArm):
        return Spec("K-TAB", "table", 0, 0, 3, False)
    return Spec("CAND", model.cell, model.hidden, 0, model.outputs, False)
