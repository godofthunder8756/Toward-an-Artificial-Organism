"""Opt-in H10 secondary transfer; no training, evaluation or data on import.

The new head reads only the intact consumer-visible representation, public
context zero and one independent private BSC(1/5) factor-four reading. Truth
is retained by the evaluator and never passed to the head or frozen arm.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Mapping, cast

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from phase3b.execution import source_hashes
from phase3b.freeze import verify_preflight_snapshot
from phase3b.models import Arm
from phase3b.resources import Meter, linear_meter, observed
from phase3b.world import generate


TRAIN_EPISODES = 2048
EVAL_EPISODES = 4096
BATCH = 32
TRANSFER_STREAM = 30_000
# The declared primary grid searches widths 1..96. Fixed padded input gives
# every arm the SAME 780-parameter, 778-MAC linear head, including word arms.
# Padding is zero, not an additional sensory channel; connected (not
# necessarily active) parameters and actual read bits are disclosed.
HEAD_INPUTS = 4 * 96 + 5


@dataclass(frozen=True)
class SecondaryData:
    common: torch.Tensor
    private_bit: torch.Tensor
    label: torch.Tensor  # evaluator only; never an input to TransferHead


def _fresh_bit(truth: torch.Tensor, seed: int) -> torch.Tensor:
    """Independent RNG, not one of the world's existing three local sensors."""
    flips = np.random.default_rng(np.random.SeedSequence([TRANSFER_STREAM + seed, 4, 0]))
    noise = torch.from_numpy((flips.random(truth.shape[0]) < 0.2).astype(np.int64))
    return truth[:, 3].long() ^ noise


def secondary_data(seed: int) -> SecondaryData:
    """One separate stream; first 2048 for fit, last 4096 for evaluation."""
    if seed not in range(1000, 1016):
        raise ValueError("H10 requires a declared final seed")
    episode = generate(TRANSFER_STREAM + seed, TRAIN_EPISODES + EVAL_EPISODES)
    return SecondaryData(episode.common, _fresh_bit(episode.truth, seed),
                         episode.truth[:, 3].clone())


def require_transfer_authorization(authorization: Mapping[str, object] | None) -> None:
    """Current source and independently audited final checkpoint provenance."""
    if (authorization is None or authorization.get("phase") != "secondary_transfer"
            or authorization.get("approved") is not True
            or authorization.get("source_sha256") != source_hashes()
            or authorization.get("final_audit_passed") is not True
            or not isinstance(authorization.get("checkpoint_sha256"), str)
            or not isinstance(authorization.get("snapshot_path"), str)
            or not isinstance(authorization.get("snapshot_sha256"), str)):
        raise RuntimeError("H10 secondary transfer not authorized for current source hashes; STOP")
    verify_preflight_snapshot(Path(cast(str, authorization["snapshot_path"])),
                              cast(str, authorization["snapshot_sha256"]))


def _state_bytes(module: nn.Module) -> str:
    """Stable digest of tensor names, shapes, dtypes and raw bytes (not flags)."""
    digest = hashlib.sha256()
    for name, tensor in sorted(module.state_dict().items()):
        value = tensor.detach().cpu().contiguous()
        digest.update(name.encode("utf-8") + b"\0")
        digest.update(str(tuple(value.shape)).encode("ascii") + b"\0")
        digest.update(str(value.dtype).encode("ascii") + b"\0")
        digest.update(value.reshape(-1).view(torch.uint8).numpy().tobytes())
    return digest.hexdigest()


class TransferHead(nn.Module):
    """Equal-size read-only head with no route to original heads or truth.

    R3's private specialist MUST be declared before reading any episodes;
    other R3 private states cannot be concatenated or pooled.
    """
    def __init__(self, arm: Arm, *, r3_specialist: int | None = None):
        super().__init__()
        if not isinstance(arm, Arm):
            raise TypeError("transfer requires an existing learned Arm")
        if arm.name == "R3":
            if r3_specialist not in (0, 1, 2):
                raise ValueError("R3 must declare exactly one private specialist")
        elif r3_specialist is not None:
            raise ValueError("R3 specialist declaration is only legal for R3")
        if arm.name == "R4" and arm.route is None:
            raise ValueError("R4 needs its frozen, training-selected public route")
        self.r3_specialist = r3_specialist
        self.feature_count = (13 if arm.word_arm else
                              4 * arm.width + 5 if arm.name == "R1" else arm.width + 5)
        if self.feature_count > HEAD_INPUTS:
            raise ValueError("intact representation exceeds prespecified equal head capacity")
        self.classifier = nn.Linear(HEAD_INPUTS, 2)
        # Assign last: the source is an external dependency, not a submodule.
        # head.parameters() can contain only classifier weights.
        object.__setattr__(self, "_source_arm", arm)

    @property
    def source_arm(self) -> Arm:
        """Unregistered source, excluded from new-head parameters and optimizer."""
        return cast(Arm, object.__getattribute__(self, "_source_arm"))

    @property
    def read_bits(self) -> int:
        return (3 if self.source_arm.word_arm else
            (4 if self.source_arm.name == "R1" else 1) * self.source_arm.width * 32)

    def features(self, common: torch.Tensor, private_bit: torch.Tensor) -> torch.Tensor:
        if (common.ndim != 2 or common.shape[1] != 8 or private_bit.shape != (common.shape[0],)
                or not torch.all((private_bit == 0) | (private_bit == 1))):
            raise ValueError("expected eight common readings and one binary private bit per episode")
        with torch.no_grad():
            states = self.source_arm.encode(common)
            if self.source_arm.word_arm:
                word, _, _, _ = self.source_arm.write(states, 1)
                if word.shape != (common.shape[0], 1) or torch.any((word < 0) | (word >= 8)):
                    raise AssertionError("not an intact three-bit word")
                visible = F.one_hot(word[:, 0].long(), 8).float()
            elif self.source_arm.name == "R3":
                visible = states[:, self.r3_specialist]
            elif self.source_arm.name == "R1":
                visible = states.flatten(1)
            else:
                visible = states
            public = torch.zeros((common.shape[0], 4), device=common.device)
            public[:, 0] = 1  # context 0, never a learned or private signal
            feature = torch.cat((visible, public, private_bit.float().unsqueeze(-1)), -1)
            if feature.shape != (common.shape[0], self.feature_count):
                raise AssertionError("consumer-visible interface dimension mismatch")
            return F.pad(feature, (0, HEAD_INPUTS - self.feature_count))

    def forward(self, common: torch.Tensor, private_bit: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(common, private_bit))


@torch.no_grad()
def _checkpoint_risks(head: TransferHead, data: SecondaryData,
                      checkpoints: list[tuple[int, dict[str, torch.Tensor]]],
                      head_meter: Meter, core_meter: Meter) -> list[dict[str, int | float]]:
    """Score every fixed checkpoint AFTER fitting; no evaluation feedback."""
    head.eval()
    curve = []
    for seen, weights in checkpoints:
        head.classifier.load_state_dict(weights)
        errors = 0
        for start in range(TRAIN_EPISODES, TRAIN_EPISODES + EVAL_EPISODES, 128):
            end = start + 128
            with linear_meter(head.source_arm, core_meter):
                features = head.features(data.common[start:end], data.private_bit[start:end])
            with linear_meter(head.classifier, head_meter):
                logits = head.classifier(features)
            errors += int((logits.argmax(-1) != data.label[start:end]).sum())
        curve.append({"training_samples": seen, "errors": errors,
                      "episodes": EVAL_EPISODES, "risk": errors / EVAL_EPISODES})
    return curve


def fit_transfer(arm: Arm, seed: int, *, authorization: Mapping[str, object] | None = None,
                 r3_specialist: int | None = None) -> dict:
    """Opt-in only: 64 batches of 32, then disjoint fixed-checkpoint scoring.

    The passed arm must already contain independently trained final weights;
    this function does not load, select, or train that arm. Evaluation labels
    are unavailable until all optimizer updates and snapshots have finished.
    """
    require_transfer_authorization(authorization)  # before data, RNG or fit
    if seed not in range(1000, 1016):
        raise ValueError("H10 requires a declared final seed")
    original = _state_bytes(arm)
    if authorization is None or authorization.get("checkpoint_sha256") != original:
        raise RuntimeError("H10 final checkpoint provenance mismatch; STOP")
    original_heads = _state_bytes(arm.heads)
    arm.eval()
    arm.requires_grad_(False)
    # fork_rng keeps the caller's initialization RNG unmodified; an arm's
    # original weights and buffers are never in this optimizer.
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        head = TransferHead(arm, r3_specialist=r3_specialist)
    data = secondary_data(seed)
    optimizer = torch.optim.AdamW(head.classifier.parameters(), lr=0.001, weight_decay=0)
    train_core, train_head = Meter(), Meter()
    checkpoints = [(0, {k: v.detach().clone() for k, v in head.classifier.state_dict().items()})]
    head.classifier.train()  # do not recursively switch the frozen arm back to train mode
    for start in range(0, TRAIN_EPISODES, BATCH):
        end = start + BATCH
        with linear_meter(arm, train_core):
            features = head.features(data.common[start:end], data.private_bit[start:end])
        with linear_meter(head.classifier, train_head):
            logits = head.classifier(features)
            objective = F.cross_entropy(logits, data.label[start:end])
            optimizer.zero_grad(set_to_none=True)
            objective.backward()
            torch.nn.utils.clip_grad_norm_(head.classifier.parameters(), 1)
            optimizer.step()
        checkpoints.append((end, {k: v.detach().clone()
                                  for k, v in head.classifier.state_dict().items()}))
    if len(checkpoints) != 65 or checkpoints[-1][0] != TRAIN_EPISODES:
        raise AssertionError("secondary episode allowance violated; STOP")
    eval_core, eval_head = Meter(), Meter()
    curve = _checkpoint_risks(head, data, checkpoints, eval_head, eval_core)
    if _state_bytes(arm) != original or _state_bytes(arm.heads) != original_heads:
        raise AssertionError("frozen original arm/heads changed; STOP")
    require_transfer_authorization(authorization)  # reject source drift during execution
    extra_params = sum(p.numel() for p in head.classifier.parameters())
    return {
        "family": arm.name, "seed": seed, "r3_specialist": r3_specialist,
        "secondary_stream": TRANSFER_STREAM + seed,
        "training_episodes": TRAIN_EPISODES, "evaluation_episodes": EVAL_EPISODES,
        "training_context": 0, "optimizer_updates": 64,
        "samples_to_risk": curve, "final_risk": curve[-1]["risk"],
        "original_arm_sha256_before_after": (original, _state_bytes(arm)),
        "original_heads_sha256_before_after": (original_heads, _state_bytes(arm.heads)),
        "original_heads_byte_identical": True,
        "intact_read_bits": head.read_bits, "fresh_private_read_bits": 1,
        "total_read_bits": head.read_bits + 1,
        "extra_trainable_parameters": extra_params,
        "parameters_connected_to_unpadded_inputs": 2 * head.feature_count + 2,
        "inactive_padding_parameters": 2 * (HEAD_INPUTS - head.feature_count),
        "extra_parameter_bytes": sum(p.numel() * p.element_size()
                                     for p in head.classifier.parameters()),
        "optimizer_state_bytes": sum(v.numel() * v.element_size()
                                     for state in optimizer.state.values()
                                     for v in state.values() if isinstance(v, torch.Tensor)),
        "training_core_forward_macs": train_core.forward_macs,
        "training_new_head_forward_macs": train_head.forward_macs,
        "training_new_head_backward_macs": train_head.backward_macs,
        "inference_core_forward_macs_per_episode": eval_core.forward_macs // (65 * EVAL_EPISODES),
        "inference_new_head_forward_macs_per_episode": eval_head.forward_macs // (65 * EVAL_EPISODES),
        "inference_total_forward_macs_per_episode": (eval_core.forward_macs + eval_head.forward_macs)
                                // (65 * EVAL_EPISODES),
        "checkpoint_evaluation_core_forward_macs": eval_core.forward_macs,
        "checkpoint_evaluation_new_head_forward_macs": eval_head.forward_macs,
        "training_core_operations": observed(train_core),
        "training_head_operations": observed(train_head),
        "evaluation_core_operations": observed(eval_core),
        "evaluation_head_operations": observed(eval_head),
        "compute_limitations": "Linear MACs and annotated forward work only; generator, loss, "
                               "backward nonlinear kernels, clipping, optimizer and actual memory traffic "
                               "are not metered. No original head executes on transfer inference.",
    }