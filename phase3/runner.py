"""Phase-III runner: train, evaluate, store, audit, replay.

Deterministic end-to-end driver shared by the engineering entry point and the
audit/replay tools. Training is per model seed (``seed_all``); evaluation runs
the six arms on the *same* episodes (observation equality) and computes the
frozen endpoints (probe/clean accuracy, incoherence rate, pi-cut decay,
novel-consumer scores). Raw results are stored as JSONL rows with a
``pre_run_snapshot.json`` (sha256 of sources + protocol) — never overwriting a
frozen results dir (``mkdir(exist_ok=False)``).
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn

import bridge.reproducibility as _rep

from phase3.arms import Arm, apply_specialists, compute_thresholds
from phase3.config import Phase3Config
from phase3.model import Encoder
from phase3.novel_consumer import novel_consumer_scores, posterior_entropy_ceiling
from phase3.task import Quantizer, sample_episodes, token_stream_to_s

__all__ = ["train_arm", "evaluate_arm", "endpoints", "state_hash", "make_snapshot",
           "write_results", "build_arm", "save_checkpoint", "load_checkpoint"]

ARM_NAMES = ["candidate", "r1", "r4", "r5", "r2", "r3"]


def state_hash(rows: object) -> str:
    """Deterministic hash of a JSON-serializable structure (replay identity)."""
    return hashlib.sha256(
        json.dumps(rows, sort_keys=True, default=_json_default).encode("utf-8")
    ).hexdigest()


def _json_default(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, torch.Tensor):
        return o.detach().cpu().numpy().tolist()
    raise TypeError(f"not serializable: {type(o)}")


def build_arm(cfg: Phase3Config, name: str, seed: int) -> Arm:
    """Build and (for learned arms) train one arm under a model seed."""
    _rep.seed_all(seed)
    if name == "candidate":
        enc = Encoder(cfg)
        train_encoder(cfg, enc, cfg.training.steps, cfg.training.lr, seed, "enc")
        return Arm(cfg, encoders={"enc": enc}, arm_name="candidate")
    if name == "r1":
        from phase3.config import r1_split_hidden
        r1_hidden = r1_split_hidden(cfg)
        encs = {}
        for i in range(cfg.arm.n_specialists):
            e = Encoder(cfg, hidden_size=r1_hidden)
            train_encoder(cfg, e, cfg.training.steps, cfg.training.lr, seed + 1000 * (i + 1), f"enc{i}")
            encs[f"enc{i}"] = e
        return Arm(cfg, encoders=encs, arm_name="r1")
    if name == "r2":
        rnn = nn.GRU(cfg.task.n_tokens, cfg.arm.r2_hidden, batch_first=False)
        heads = train_heads_r2r3(cfg, rnn, kind="r2", seed=seed)
        return Arm(cfg, encoders={"rnn": rnn, **{f"head_{k}": v for k, v in heads.items()}},
                   arm_name="r2")
    if name == "r3":
        readers = [nn.GRU(cfg.task.n_tokens, cfg.arm.r3_hidden, batch_first=False)
                   for _ in range(cfg.arm.n_specialists)]
        heads = train_heads_r2r3(cfg, readers, kind="r3", seed=seed)
        encs = {f"reader{i}": readers[i] for i in range(cfg.arm.n_specialists)}
        encs.update({f"head_{k}": v for k, v in heads.items()})
        return Arm(cfg, encoders=encs, arm_name="r3")
    if name in ("r4", "r5"):
        return Arm(cfg, encoders={}, arm_name=name)
    raise ValueError(name)


def train_encoder(cfg, enc, steps, lr, seed, name):
    from phase3.train import train_encoder as _te
    _te(cfg, enc, steps, lr, seed, name)


def train_heads_r2r3(cfg: Phase3Config, modules, kind: str, seed: int) -> nn.ModuleDict:
    from phase3.train import r2_heads, r3_heads, train_r2, train_r3
    if kind == "r2":
        heads = r2_heads(cfg, cfg.arm.r2_hidden)
        train_r2(cfg, modules, heads, cfg.training.steps, cfg.training.lr, seed)
        return heads
    heads = r3_heads(cfg, cfg.arm.r3_hidden)
    train_r3(cfg, modules, heads, cfg.training.steps, cfg.training.lr, seed)
    return heads


def evaluate_arm(cfg: Phase3Config, arm: Arm, x: np.ndarray, z: np.ndarray,
                 thr: Dict[str, float]) -> Dict[str, object]:
    """Frozen endpoints for one arm on a fixed episode set (per seed, planned denominator)."""
    tr = arm.run(x)
    regime = tr["regime"]
    probe_entry = cfg.task.horizon - cfg.task.probe_window

    if arm.has_w:
        w = tr["w"]
        out = apply_specialists(w, cfg, thr, regime)
        spol, splan, sreg = out["spol"], out["splan"], out["sreg"]
        # probe accuracy: S_pol at the final step (t = H), where W is the only carrier
        final = spol[..., -1]
        probe_acc = float(np.mean(final == z))
        # clean (accumulation) accuracy: S_pol at the last informative step
        clean_acc = float(np.mean(spol[..., probe_entry - 1] == z))
        inc = _incoherence_rate(cfg, thr, w, regime)
        # pi-cut decay: run with cut_pi and re-measure probe accuracy
        tr_cut = arm.run(x, cut_pi=True)
        w_cut = tr_cut["w"]
        out_cut = apply_specialists(w_cut, cfg, thr, regime)
        cut_acc = float(np.mean(out_cut["spol"][..., -1] == z))
        novel = novel_consumer_scores(cfg, w, z, thr)
        s_h = token_stream_to_s(cfg.task, x)[..., -1]
        ceil = posterior_entropy_ceiling(cfg, s_h, z)
        return {
            "arm": arm.arm_name, "probe_acc": probe_acc, "clean_acc": clean_acc,
            "incoherence_rate": inc, "pi_cut_probe_acc": cut_acc,
            "s_conf_log_loss": novel["s_conf_log_loss"],
            "s_bias_accuracy": novel["s_bias_accuracy"],
            "s_conf_ceiling": ceil,
        }

    # R2/R3: learned heads produce the outputs from the rich state.
    spol, splan, sreg = _head_outputs(cfg, arm, x)
    final = spol[..., -1]
    return {
        "arm": arm.arm_name,
        "probe_acc": float(np.mean(final == z)),
        "clean_acc": float(np.mean(spol[..., probe_entry - 1] == z)),
        "incoherence_rate": _incoherence_rate_from_outputs(cfg, thr, spol, splan, sreg),
        "pi_cut_probe_acc": None,
        "s_conf_log_loss": None, "s_bias_accuracy": None, "s_conf_ceiling": None,
    }


def _head_outputs(cfg: Phase3Config, arm: Arm, x: np.ndarray):
    """R2/R3 specialist outputs from the learned heads (argmax over logits)."""
    import torch.nn.functional as F
    B, H = x.shape
    x_t = torch.from_numpy(x).long()
    x_oh = F.one_hot(x_t, num_classes=cfg.task.n_tokens).float()
    device = next(iter(arm.encoders.values())).parameters().__next__().device

    def head_out(name, h):
        head = arm.encoders[f"head_{name}"]
        from phase3.train import _context_inputs
        logits = head(_context_inputs(cfg, x_oh, h, name))
        return logits.argmax(-1).detach().cpu().numpy()

    if arm.arm_name == "r2":
        out, _ = arm.encoders["rnn"](x_oh.transpose(0, 1))
        h = out.transpose(0, 1)
        return head_out("spol", h), head_out("splan", h), head_out("sreg", h)
    names = ["spol", "splan", "sreg"]
    outs = []
    for i, name in enumerate(names):
        out, _ = arm.encoders[f"reader{i}"](x_oh.transpose(0, 1))
        h = out.transpose(0, 1)
        outs.append(head_out(name, h))
    return outs[0], outs[1], outs[2]


def _manifold(cfg: Phase3Config, thr: Dict[str, float]):
    """The six realizable triples of the shared-content manifold (G6 §2.1)."""
    from phase3.specialists import MANIFOLD_TRIPLES
    return MANIFOLD_TRIPLES


def _incoherence_rate(cfg: Phase3Config, thr: Dict[str, float], w: np.ndarray,
                      regime: np.ndarray) -> float:
    out = apply_specialists(w, cfg, thr, regime)
    return _incoherence_rate_from_outputs(cfg, thr, out["spol"], out["splan"], out["sreg"])


def _incoherence_rate_from_outputs(cfg, thr, spol, splan, sreg) -> float:
    m = _manifold(cfg, thr)
    flat = np.stack([spol.reshape(-1), splan.reshape(-1), sreg.reshape(-1)], axis=-1)
    on = np.array([tuple(r) in m for r in flat])
    return float(1.0 - np.mean(on))


def endpoints(cfg: Phase3Config, arms: Dict[str, Arm], seed: int,
              n_episodes: int) -> List[Dict[str, object]]:
    """Evaluate all arms on the same episode set (observation equality)."""
    z, x = sample_episodes(cfg.task, n_episodes, seed)
    thr = compute_thresholds(cfg)
    rows = []
    for name in ARM_NAMES:
        row = evaluate_arm(cfg, arms[name], x, z, thr)
        row["seed"] = seed
        row["n_episodes"] = n_episodes
        rows.append(row)
    return rows


def make_snapshot(out_dir: str, cfg: Phase3Config, sources: List[str]) -> str:
    """Write pre_run_snapshot.json: sha256 of every source + the config."""
    snap = {"config": cfg.to_dict(), "sources": {}}
    for src in sources:
        with open(src, "rb") as fh:
            snap["sources"][src] = hashlib.sha256(fh.read()).hexdigest()
    path = os.path.join(out_dir, "pre_run_snapshot.json")
    with open(path, "w") as fh:
        json.dump(snap, fh, indent=2, default=_json_default)
    return path


def write_results(out_dir: str, cfg: Phase3Config, rows: List[Dict[str, object]],
                  snapshot_sources: List[str]) -> Dict[str, str]:
    """Write results.json and rows.jsonl into a fresh (exist_ok=False) dir."""
    os.makedirs(out_dir, exist_ok=False)
    make_snapshot(out_dir, cfg, snapshot_sources)
    with open(os.path.join(out_dir, "rows.jsonl"), "w") as fh:
        for row in rows:
            fh.write(json.dumps(row, default=_json_default) + "\n")
    results = {"version": cfg.version, "n_rows": len(rows),
               "state_hash": state_hash(rows)}
    with open(os.path.join(out_dir, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2, default=_json_default)
    return {"rows.jsonl": os.path.join(out_dir, "rows.jsonl"),
            "results.json": os.path.join(out_dir, "results.json"),
            "pre_run_snapshot.json": os.path.join(out_dir, "pre_run_snapshot.json")}


def save_checkpoint(arm: Arm, path: str) -> None:
    """Persist the arm's learned-module state dicts (resumability / replay)."""
    state = {k: v.state_dict() for k, v in arm.encoders.items()
             if hasattr(v, "state_dict")}
    torch.save({"arm": arm.arm_name, "modules": state}, path)


def load_checkpoint(arm: Arm, path: str) -> None:
    """Restore the arm's learned-module state dicts from a checkpoint."""
    ck = torch.load(path, weights_only=False)
    for k, sd in ck["modules"].items():
        if k in arm.encoders:
            arm.encoders[k].load_state_dict(sd)
