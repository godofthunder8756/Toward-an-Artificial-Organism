"""Episode sampling and the fixed Adam budget.

CAND, F-INIT and F-TRAINED reject TEST only. Selection rejects TEST and VAL.
Each run reseeds an independent generator at 1000+s.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import torch

from recurrent_core_transfer_spec import (
    ADAM_BETA1,
    ADAM_BETA2,
    ADAM_EPS,
    BATCH,
    GRAD_CLIP,
    STEPS,
    is_val_history,
)
from twostream_acquisition_spec import cosine_lr, is_test_history
from twostream_acquisition_train import episodes_from_uniforms


def reject_mask(include_val: bool) -> torch.Tensor:
    return torch.tensor(
        [is_test_history(h) or (include_val and is_val_history(h)) for h in range(256)],
        dtype=torch.bool,
    )


def sample_batch(generator: torch.Generator, batch: int, reject: torch.Tensor):
    """Rejection-sample `batch` episodes. Rejected draws are not reused."""
    kept_bits = []
    kept_labels = []
    accepted = 0
    empty_draws = 0
    while accepted < batch:
        draw = batch - accepted
        uniforms = torch.rand((draw, 31), dtype=torch.float64, generator=generator)
        bits, labels, history = episodes_from_uniforms(uniforms)
        keep = ~reject[history]
        if bool(keep.any()):
            kept_bits.append(bits[keep])
            kept_labels.append(labels[keep])
            accepted += int(keep.sum())
            empty_draws = 0
        else:
            empty_draws += 1
            if empty_draws > 10000:
                raise RuntimeError("episode rejection accepted nothing")
    bits = torch.cat(kept_bits, dim=0)[:batch].to(torch.float32)
    labels = torch.cat(kept_labels, dim=0)[:batch].to(torch.float32)
    return bits, labels


def train_arm(
    model: torch.nn.Module,
    episode_seed: int,
    freeze_recurrent: bool,
    include_val_reject: bool,
    steps: int = STEPS,
    batch: int = BATCH,
) -> dict:
    torch.set_num_threads(1)
    if freeze_recurrent:
        for parameter in model.recurrent_parameters():
            parameter.requires_grad_(False)
    else:
        for parameter in model.recurrent_parameters():
            parameter.requires_grad_(True)
    for parameter in model.readout_parameters():
        parameter.requires_grad_(True)
    parameters = [parameter for parameter in model.parameters() if parameter.requires_grad]
    optimizer = torch.optim.Adam(
        parameters,
        lr=cosine_lr(0, steps),
        betas=(ADAM_BETA1, ADAM_BETA2),
        eps=ADAM_EPS,
        weight_decay=0.0,
    )
    generator = torch.Generator(device="cpu")
    generator.manual_seed(1000 + episode_seed)
    reject = reject_mask(include_val_reject)
    model.train()
    last_loss = None
    for step in range(steps):
        learning_rate = cosine_lr(step, steps)
        for group in optimizer.param_groups:
            group["lr"] = learning_rate
        bits, labels = sample_batch(generator, batch, reject)
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
        "include_val_reject": include_val_reject,
        "episode_seed": 1000 + episode_seed,
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
        "include_val_reject": None,
        "episode_seed": None,
    }
