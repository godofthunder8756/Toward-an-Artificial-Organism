"""R-FIX training and the synthetic freezing fixture.

CAND calls the unchanged PR #7 train_arm. R-FIX freezes only rnn.weight_hh_l0.
No consciousness claim.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import torch

import recurrent_core_transfer_train as rct_train
from recurrent_core_transfer_models import (
    build_initialized,
    checkpoint_sha256,
    load_checkpoint,
    save_checkpoint,
    snapshot_state,
)
from recurrent_core_transfer_spec import (
    ADAM_BETA1,
    ADAM_BETA2,
    ADAM_EPS,
    BATCH,
    GRAD_CLIP,
    STEPS,
)
from recurrent_core_transfer_train import reject_mask, sample_batch, train_arm
from twostream_acquisition_spec import cosine_lr

from frozen_recurrent_compensation_spec import (
    ARM_HIDDEN,
    ARMS,
    EXPECTED_COUNTS,
    FIXTURE_BATCH,
    FIXTURE_DATA_SEED,
    FIXTURE_SEED,
    FIXTURE_STEPS,
    SEEDS,
)

HH_NAME = "rnn.weight_hh_l0"
GRU_KEYS = (
    "rnn.weight_ih_l0",
    "rnn.weight_hh_l0",
    "rnn.bias_ih_l0",
    "rnn.bias_hh_l0",
)


class FreezeCheckError(RuntimeError):
    pass


def configure_runtime() -> None:
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def tensor_sha256(tensor: torch.Tensor) -> str:
    array = tensor.detach().cpu().contiguous()
    if array.dtype != torch.float32:
        raise RuntimeError("W0 byte hash expects float32, got %s" % array.dtype)
    return hashlib.sha256(array.numpy().tobytes()).hexdigest()


class Digester:
    """sha256 of accepted float32 bit bytes then label bytes, step by step."""

    def __init__(self, batch: int):
        self.batch = int(batch)
        self._hash = hashlib.sha256()
        self.n = 0

    def update(self, bits: torch.Tensor, labels: torch.Tensor) -> None:
        bit_array = bits.detach().cpu().contiguous()
        label_array = labels.detach().cpu().contiguous()
        if bit_array.dtype != torch.float32 or label_array.dtype != torch.float32:
            raise RuntimeError("digest expects float32 batches")
        if tuple(bit_array.shape) != (self.batch, 8) or tuple(label_array.shape) != (self.batch, 3):
            raise RuntimeError((tuple(bit_array.shape), tuple(label_array.shape)))
        self._hash.update(bit_array.numpy().tobytes())
        self._hash.update(label_array.numpy().tobytes())
        self.n += 1

    def hexdigest(self) -> str:
        return self._hash.hexdigest()


def episode_stream_digest(episode_seed: int, steps: int = STEPS, batch: int = BATCH) -> str:
    """Regenerate generator 1000+s with TEST rejection only. Does not train."""
    configure_runtime()
    digester = Digester(batch)
    generator = torch.Generator(device="cpu")
    generator.manual_seed(1000 + int(episode_seed))
    reject = reject_mask(False)
    for _step in range(steps):
        bits, labels = sample_batch(generator, batch, reject)
        digester.update(bits, labels)
    if digester.n != steps:
        raise RuntimeError(digester.n)
    return digester.hexdigest()


def configure_parameter_freeze(model, freeze_mode: str) -> None:
    if freeze_mode == "rfix":
        for name, parameter in model.named_parameters():
            parameter.requires_grad_(name != HH_NAME)
    elif freeze_mode == "extra_frozen":
        for name, parameter in model.named_parameters():
            parameter.requires_grad_(name not in (HH_NAME, "rnn.weight_ih_l0"))
    elif freeze_mode == "hh_trainable":
        for parameter in model.parameters():
            parameter.requires_grad_(True)
    else:
        raise ValueError(freeze_mode)


def frozen_parameter_names(model) -> list[str]:
    return [name for name, parameter in model.named_parameters() if not parameter.requires_grad]


def assert_only_weight_hh_frozen(model) -> None:
    frozen = frozen_parameter_names(model)
    if frozen != [HH_NAME]:
        raise FreezeCheckError("frozen set is not exactly rnn.weight_hh_l0: %s" % frozen)
    if model.rnn.weight_hh_l0.requires_grad:
        raise FreezeCheckError("weight_hh requires_grad is not False")


def assert_optimizer_excludes_hh(model, optimizer) -> None:
    optimizer_ids = {id(parameter) for group in optimizer.param_groups for parameter in group["params"]}
    if id(model.rnn.weight_hh_l0) in optimizer_ids:
        raise FreezeCheckError("weight_hh is in the optimizer")
    for name, parameter in model.named_parameters():
        if name == HH_NAME:
            continue
        if id(parameter) not in optimizer_ids:
            raise FreezeCheckError("trainable tensor absent from the optimizer: %s" % name)


def assert_hh_grad_none(model) -> None:
    if model.rnn.weight_hh_l0.grad is not None:
        raise FreezeCheckError("weight_hh.grad is not None")


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


def _guard_study_seed(episode_seed: int, steps: int, batch: int, batches, freeze_mode: str) -> None:
    if int(episode_seed) not in SEEDS:
        return
    if freeze_mode != "rfix" or batches is not None or steps != STEPS or batch != BATCH:
        raise RuntimeError("study seeds only run the full R-FIX recipe")


def train_arm_rfix(
    model,
    episode_seed: int,
    steps: int = STEPS,
    batch: int = BATCH,
    *,
    batches=None,
    freeze_mode: str = "rfix",
) -> dict:
    """PR #7 train_arm with one difference: only rnn.weight_hh_l0 is frozen.

    `batches` and `freeze_mode` other than "rfix" exist for the synthetic fixture.
    Study calls use train_arm_rfix(model, episode_seed).
    """
    _guard_study_seed(episode_seed, steps, batch, batches, freeze_mode)
    configure_runtime()
    configure_parameter_freeze(model, freeze_mode)
    assert_only_weight_hh_frozen(model)
    parameters = [parameter for parameter in model.parameters() if parameter.requires_grad]
    optimizer = torch.optim.Adam(
        parameters,
        lr=cosine_lr(0, steps),
        betas=(ADAM_BETA1, ADAM_BETA2),
        eps=ADAM_EPS,
        weight_decay=0.0,
    )
    assert_optimizer_excludes_hh(model, optimizer)
    clipped_names = []
    parameter_ids = {id(parameter) for parameter in parameters}
    for name, parameter in model.named_parameters():
        if id(parameter) in parameter_ids:
            clipped_names.append(name)
    if HH_NAME in clipped_names:
        raise FreezeCheckError("weight_hh is in the clip list")
    w0_sha = tensor_sha256(model.rnn.weight_hh_l0)
    model.rnn.weight_hh_l0.grad = None
    digester = None
    generator = None
    reject = None
    if batches is None:
        digester = Digester(batch)
        generator = torch.Generator(device="cpu")
        generator.manual_seed(1000 + int(episode_seed))
        reject = reject_mask(False)
    elif len(batches) != steps:
        raise RuntimeError("synthetic batch count does not match steps")
    model.train()
    last_loss = None
    grad_checks = 0
    freezing_failure = None
    integrity = True
    failure_step = None
    completed = 0
    for step in range(steps):
        learning_rate = cosine_lr(step, steps)
        for group in optimizer.param_groups:
            group["lr"] = learning_rate
        if batches is None:
            bits, labels = sample_batch(generator, batch, reject)
            digester.update(bits, labels)
        else:
            bits, labels = batches[step]
        optimizer.zero_grad(set_to_none=True)
        predictions = model(bits)
        loss = ((predictions - labels) ** 2).sum(dim=1).mean()
        if not torch.isfinite(loss):
            integrity = False
            failure_step = step
            break
        loss.backward()
        try:
            assert_hh_grad_none(model)
        except FreezeCheckError as exc:
            freezing_failure = str(exc)
            failure_step = step
            break
        grad_checks += 1
        if _grads_bad(parameters):
            integrity = False
            failure_step = step
            break
        torch.nn.utils.clip_grad_norm_(parameters, GRAD_CLIP)
        optimizer.step()
        if _weights_bad(parameters):
            integrity = False
            failure_step = step
            break
        if tensor_sha256(model.rnn.weight_hh_l0) != w0_sha:
            freezing_failure = "W0 bytes changed"
            failure_step = step
            break
        last_loss = float(loss.detach())
        completed = step + 1
    if completed == steps and tensor_sha256(model.rnn.weight_hh_l0) != w0_sha:
        freezing_failure = "W0 bytes changed"
    # integrity_training is the non-finite check only. A freezing stop keeps it true
    # and is reported separately. An early freezing stop has steps_completed < steps.
    checks = {
        "precheck_only_weight_hh": True,
        "precheck_requires_grad_false": True,
        "precheck_absent_from_optimizer": True,
        "grad_none_steps_checked": grad_checks,
        "grad_none_every_completed_backward": freezing_failure != "weight_hh.grad is not None",
        "w0_sha256": w0_sha,
        "w0_unchanged_after_training": freezing_failure != "W0 bytes changed" and completed == steps and integrity,
        "clipped_parameter_names": clipped_names,
        "clip_covers_trainable_only": HH_NAME not in clipped_names,
    }
    return {
        "integrity_training": bool(integrity),
        "steps_completed": completed,
        "final_loss": last_loss,
        "failure_step": failure_step,
        "include_val_reject": False,
        "episode_seed": None if batches is not None else 1000 + int(episode_seed),
        "episode_digest": None if digester is None else digester.hexdigest(),
        "batches_hashed": 0 if digester is None else digester.n,
        "freezing_checks": checks,
        "freezing_failure": freezing_failure,
        "synthetic_batches": batches is not None,
        "trainer": "train_arm_rfix",
    }


def train_cand(model, episode_seed: int, steps: int = STEPS, batch: int = BATCH) -> dict:
    """Unchanged train_arm. Batches it consumes are hashed by a temporary wrap.

    The PR #7 source file is not modified. The wrap returns the original tensors.
    """
    if int(episode_seed) in SEEDS and (steps != STEPS or batch != BATCH):
        raise RuntimeError("study seeds only run the full recipe")
    configure_runtime()
    digester = Digester(batch)
    original = rct_train.sample_batch

    def wrapped(generator, batch_size, reject):
        bits, labels = original(generator, batch_size, reject)
        digester.update(bits, labels)
        return bits, labels

    rct_train.sample_batch = wrapped
    try:
        if rct_train.train_arm.__globals__["sample_batch"] is not wrapped:
            raise RuntimeError("train_arm cannot see the sample_batch wrap")
        info = train_arm(model, episode_seed, False, False, steps=steps, batch=batch)
    finally:
        rct_train.sample_batch = original
    packed = dict(info)
    packed["episode_digest"] = digester.hexdigest()
    packed["batches_hashed"] = digester.n
    packed["freezing_checks"] = None
    packed["freezing_failure"] = None
    packed["synthetic_batches"] = False
    packed["trainer"] = "train_arm"
    packed["include_val_reject"] = False
    return packed


def counts_from_state(state: dict, arm: str) -> dict:
    stored = sum(int(tensor.numel()) for tensor in state.values())
    frozen = 0 if arm == "CAND" else int(state[HH_NAME].numel())
    return {"stored": stored, "frozen": frozen, "trainable": stored - frozen, "H": ARM_HIDDEN[arm]}


def trainable_count(model, arm: str) -> dict:
    configure_parameter_freeze(model, "rfix" if arm != "CAND" else "hh_trainable")
    if arm == "CAND":
        for parameter in model.parameters():
            parameter.requires_grad_(True)
    stored = sum(int(parameter.numel()) for parameter in model.parameters())
    trainable = sum(int(parameter.numel()) for parameter in model.parameters() if parameter.requires_grad)
    frozen = stored - trainable
    return {"stored": stored, "trainable": trainable, "frozen": frozen, "H": model.readout_hidden}


def draw_seed(seed: int) -> dict:
    """Draw CAND, R-FIX-32 and R-FIX-48 in that order and assert pairing."""
    configure_runtime()
    states = {
        "CAND": snapshot_state(build_initialized(seed, 32)),
        "R-FIX-32": snapshot_state(build_initialized(seed, 32)),
        "R-FIX-48": snapshot_state(build_initialized(seed, 48)),
    }
    assert_pairing_states(states)
    for arm in ARMS:
        counts = counts_from_state(states[arm], arm)
        if counts != EXPECTED_COUNTS[arm]:
            raise RuntimeError("parameter count mismatch for %s: %s" % (arm, counts))
    return states


def assert_pairing_states(states: dict) -> None:
    cand = states["CAND"]
    r32 = states["R-FIX-32"]
    r48 = states["R-FIX-48"]
    if not all(torch.equal(cand[key], r32[key]) for key in cand):
        raise RuntimeError("CAND and R-FIX-32 inits are not fully equal")
    if not all(torch.equal(cand[key], r48[key]) for key in GRU_KEYS):
        raise RuntimeError("GRU tensors differ between H=32 and H=48")
    if not torch.equal(cand["readout_fc1.weight"], r48["readout_fc1.weight"][:32]):
        raise RuntimeError("fc1.weight rows 0-31 are not paired")
    if torch.equal(cand["readout_fc1.bias"], r48["readout_fc1.bias"]):
        raise RuntimeError("fc1.bias was not expected to match under partial pairing")
    if cand["readout_fc2.weight"].shape == r48["readout_fc2.weight"].shape:
        raise RuntimeError("fc2.weight shape was not expected to match")
    if torch.equal(cand["readout_fc2.bias"], r48["readout_fc2.bias"]):
        raise RuntimeError("fc2.bias was not expected to match under partial pairing")
    w0 = {tensor_sha256(states[arm][HH_NAME]) for arm in ARMS}
    if len(w0) != 1:
        raise RuntimeError("W0 hash differs across arms")


def pairing_flags(seed: int) -> dict:
    states = draw_seed(seed)
    cand = states["CAND"]
    r48 = states["R-FIX-48"]
    return {
        "full_equal_cand_rfix32": True,
        "gru_equal_32_48": True,
        "fc1_rows_0_31_equal": True,
        "fc1_bias_differs": True,
        "fc2_weight_shape_differs": True,
        "fc2_bias_differs": True,
        "w0_sha256": tensor_sha256(cand[HH_NAME]),
        "fc1_rows": int(cand["readout_fc1.weight"].shape[0]),
        "fc1_rows_wide": int(r48["readout_fc1.weight"].shape[0]),
    }


def synthetic_batches(steps: int, batch: int, data_seed: int):
    generator = torch.Generator(device="cpu")
    generator.manual_seed(int(data_seed))
    batches = []
    for _step in range(steps):
        bits = torch.randint(0, 2, (batch, 8), dtype=torch.int64, generator=generator).to(torch.float32)
        labels = torch.rand((batch, 3), dtype=torch.float32, generator=generator)
        batches.append((bits, labels))
    return batches


def _expect_freeze_error(model, batches, freeze_mode: str, text: str) -> None:
    try:
        train_arm_rfix(
            model,
            FIXTURE_SEED,
            steps=1,
            batch=FIXTURE_BATCH,
            batches=batches,
            freeze_mode=freeze_mode,
        )
    except FreezeCheckError as exc:
        if text not in str(exc):
            raise
    else:
        raise RuntimeError("negative case was not caught: %s" % freeze_mode)


def run_synthetic_fixture(return_model: bool = False) -> dict:
    """Non-study seed, synthetic inputs, a few steps, and negative cases.

    This is implementation testing. It does not use seeds 400-409 or streams 1400-1409.
    """
    configure_runtime()
    negative_batches = synthetic_batches(1, FIXTURE_BATCH, FIXTURE_DATA_SEED + 1)
    _expect_freeze_error(build_initialized(FIXTURE_SEED, 32), negative_batches, "extra_frozen", "frozen set")
    _expect_freeze_error(build_initialized(FIXTURE_SEED, 32), negative_batches, "hh_trainable", "frozen set")
    grad_model = build_initialized(FIXTURE_SEED, 32)
    for parameter in grad_model.parameters():
        parameter.requires_grad_(True)
    bits, labels = negative_batches[0]
    ((grad_model(bits) - labels) ** 2).sum().backward()
    try:
        assert_hh_grad_none(grad_model)
    except FreezeCheckError as exc:
        if "grad" not in str(exc):
            raise
    else:
        raise RuntimeError("grad check was not caught")
    open_model = build_initialized(FIXTURE_SEED, 32)
    optimizer = torch.optim.Adam(open_model.parameters(), lr=1e-3)
    try:
        assert_optimizer_excludes_hh(open_model, optimizer)
    except FreezeCheckError as exc:
        if "optimizer" not in str(exc):
            raise
    else:
        raise RuntimeError("optimizer check was not caught")

    model = build_initialized(FIXTURE_SEED, 32)
    before = tensor_sha256(model.rnn.weight_hh_l0)
    ih_before = model.rnn.weight_ih_l0.detach().clone()
    info = train_arm_rfix(
        model,
        FIXTURE_SEED,
        steps=FIXTURE_STEPS,
        batch=FIXTURE_BATCH,
        batches=synthetic_batches(FIXTURE_STEPS, FIXTURE_BATCH, FIXTURE_DATA_SEED),
    )
    after = tensor_sha256(model.rnn.weight_hh_l0)
    if info["freezing_failure"] is not None or not info["integrity_training"]:
        raise RuntimeError("fixture training failed: %s" % info)
    if after != before or model.rnn.weight_hh_l0.grad is not None:
        raise RuntimeError("fixture did not keep weight_hh frozen")
    if torch.equal(model.rnn.weight_ih_l0, ih_before):
        raise RuntimeError("fixture did not train input weights")
    temporary = Path(tempfile.mkstemp(suffix=".json")[1])
    try:
        sha = save_checkpoint(temporary, snapshot_state(model))
        loaded = load_checkpoint(temporary)
        if checkpoint_sha256(loaded) != sha:
            raise RuntimeError("fixture round-trip sha mismatch")
        if tensor_sha256(loaded[HH_NAME]) != before:
            raise RuntimeError("fixture reload changed W0")
    finally:
        temporary.unlink(missing_ok=True)
    payload = {
        "passed": True,
        "negative_case_caught": True,
        "seed": FIXTURE_SEED,
        "data_seed": FIXTURE_DATA_SEED,
        "steps": FIXTURE_STEPS,
        "batch": FIXTURE_BATCH,
        "inputs": "synthetic",
        "study_seeds_used": False,
        "study_streams_used": False,
        "w0_unchanged": True,
        "w0_unchanged_after_reload": True,
        "input_weights_changed": True,
        "grad_none_steps_checked": info["freezing_checks"]["grad_none_steps_checked"],
    }
    if return_model:
        payload["model"] = model
    return payload
