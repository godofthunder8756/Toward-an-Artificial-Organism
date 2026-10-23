"""Seeded episode sampling and the fixed 4000-step Adam budget.

Sampling is rejection sampling of the generative model. Only accepted TRAIN
histories count toward the episode budget. CAND and K-FR share the sampler
seed 1000+s, so a shared code path produces the same episodes.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import torch

from fractions import Fraction

from twostream_acquisition_spec import (
    ADAM_BETA1,
    ADAM_BETA2,
    ADAM_EPS,
    BATCH,
    GRAD_CLIP,
    STEPS,
    Spec,
    cosine_lr,
)

# Exact float64 values of the protocol probabilities.
P_HALF = float(Fraction(1, 2))
P_COMMON = float(Fraction(1, 5))
P_DX = float(Fraction(1, 50))
P_DY = float(Fraction(1, 40))
P_NOISE = P_COMMON


def episodes_from_uniforms(uniforms: torch.Tensor):
    """Decode a (batch, 31) block of float64 uniforms into episodes.

    Column layout: initial X, initial Y, then for each of 8 readings a noise
    bit, and after each of the first 7 readings the triple (C, Dx, Dy).
    """
    if uniforms.ndim != 2 or uniforms.shape[1] != 31:
        raise ValueError(tuple(uniforms.shape))
    x = (uniforms[:, 0] < P_HALF).to(torch.int64)
    y = (uniforms[:, 1] < P_HALF).to(torch.int64)
    observations = []
    column = 2
    for stage in range(8):
        truth = x if stage % 2 == 0 else y
        flip = (uniforms[:, column] < P_NOISE).to(torch.int64)
        column += 1
        observations.append(truth ^ flip)
        if stage < 7:
            common = (uniforms[:, column] < P_COMMON).to(torch.int64)
            column += 1
            dx = (uniforms[:, column] < P_DX).to(torch.int64)
            column += 1
            dy = (uniforms[:, column] < P_DY).to(torch.int64)
            column += 1
            x = x ^ common ^ dx
            y = y ^ common ^ dy
    if column != 31:
        raise RuntimeError(column)
    bits = torch.stack(observations, dim=1)
    history = torch.zeros(bits.shape[0], dtype=torch.int64)
    for stage in range(8):
        history = history | (bits[:, stage] << stage)
    labels = torch.stack([x, y, x ^ y], dim=1)
    return bits.to(torch.float64), labels.to(torch.float64), history


def test_mask_tensor() -> torch.Tensor:
    from twostream_acquisition_spec import is_test_history

    return torch.tensor([is_test_history(h) for h in range(256)], dtype=torch.bool)


_TEST_MASK = None


def sample_batch(generator: torch.Generator, batch: int, test_mask: torch.Tensor | None = None):
    """Rejection-sample `batch` TRAIN episodes. Rejected draws are not reused."""
    global _TEST_MASK
    if test_mask is None:
        if _TEST_MASK is None:
            _TEST_MASK = test_mask_tensor()
        test_mask = _TEST_MASK
    kept_bits = []
    kept_labels = []
    accepted = 0
    while accepted < batch:
        draw = batch - accepted
        uniforms = torch.rand((draw, 31), dtype=torch.float64, generator=generator)
        bits, labels, history = episodes_from_uniforms(uniforms)
        keep = ~test_mask[history]
        if bool(keep.any()):
            kept_bits.append(bits[keep])
            kept_labels.append(labels[keep])
            accepted += int(keep.sum())
    bits = torch.cat(kept_bits, dim=0)[:batch].to(torch.float32)
    labels = torch.cat(kept_labels, dim=0)[:batch].to(torch.float32)
    return bits, labels


def trainable_parameters(model: torch.nn.Module, freeze_recurrent: bool):
    if freeze_recurrent:
        for parameter in model.recurrent_parameters():
            parameter.requires_grad_(False)
    else:
        for parameter in model.recurrent_parameters():
            parameter.requires_grad_(True)
    for parameter in model.readout_parameters():
        parameter.requires_grad_(True)
    return [parameter for parameter in model.parameters() if parameter.requires_grad]


def train_model(model: torch.nn.Module, spec: Spec, steps: int = STEPS, batch: int = BATCH) -> dict:
    """Adam for `steps` updates. A non-finite loss or weight is an integrity failure.

    The caller has already seeded torch and constructed `model`. This function
    does not reseed the global generator.
    """
    torch.set_num_threads(1)
    parameters = trainable_parameters(model, spec.freeze_recurrent)
    optimizer = torch.optim.Adam(
        parameters,
        lr=cosine_lr(0, steps),
        betas=(ADAM_BETA1, ADAM_BETA2),
        eps=ADAM_EPS,
    )
    generator = torch.Generator(device="cpu")
    generator.manual_seed(1000 + spec.seed)
    model.train()
    last_loss = None
    for step in range(steps):
        learning_rate = cosine_lr(step, steps)
        for group in optimizer.param_groups:
            group["lr"] = learning_rate
        bits, labels = sample_batch(generator, batch)
        optimizer.zero_grad(set_to_none=True)
        predictions = model(bits)
        loss = ((predictions - labels) ** 2).sum(dim=1).mean()
        if not torch.isfinite(loss):
            return _failure(step, last_loss)
        loss.backward()
        if _grads_bad(parameters):
            return _failure(step, float(loss.detach()))
        torch.nn.utils.clip_grad_norm_(parameters, GRAD_CLIP)
        optimizer.step()
        if _weights_bad(parameters):
            return _failure(step, float(loss.detach()))
        last_loss = float(loss.detach())
    return {
        "integrity_training": True,
        "steps_completed": steps,
        "final_loss": last_loss,
        "failure_step": None,
    }


def _grads_bad(parameters) -> bool:
    for parameter in parameters:
        if parameter.grad is not None and not torch.isfinite(parameter.grad).all():
            return True
    return False


def _weights_bad(parameters) -> bool:
    for parameter in parameters:
        if not torch.isfinite(parameter).all():
            return True
    return False


def _failure(step: int, last_loss) -> dict:
    return {
        "integrity_training": False,
        "steps_completed": step,
        "final_loss": last_loss,
        "failure_step": step,
    }
