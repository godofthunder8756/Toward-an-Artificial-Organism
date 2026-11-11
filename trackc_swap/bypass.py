"""Track C swap, option K step 1: locate the erasure bypass in saved agents (no training).

Additive module; every earlier module is unchanged. An agent is loaded from saved
weights and run in the v6 world (echo-free, SAT gain, wear 0.001) under:

  intact      no erasure;
  full        the carried state is erased with probability `rate` every step, as in
              v4-v6's "imposed full erasure" evaluation;
  memoryless  the carried state is erased every step, so each action depends on the
              current observation only.

Within `full` and `memoryless`, one channel group of the observation is shuffled
across environments on the steps just before and at each probe (`window` steps,
ending at the probe step). The shuffle keeps each channel's distribution and
destroys its relation to that environment's cue. If accuracy falls, the agent read
the cue bit from that channel. Groups: walls (25), food (25), intero (1), view
(walls + food) and all (view + intero). The echo channels are zero in this world.

Also recorded (descriptive): the agent's cell at each probe, for a cell-majority
decoder of the target, and interoception at each probe by target.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from .env import VIEW, WorldConfig
from .erasure import ErasureAgent, NoEchoSwapWorld

N_CELLS = VIEW * VIEW
GROUPS = {
    "walls": list(range(0, N_CELLS)),
    "food": list(range(N_CELLS, 2 * N_CELLS)),
    "intero": [2 * N_CELLS],
}
GROUPS["view"] = GROUPS["walls"] + GROUPS["food"]
GROUPS["all"] = GROUPS["view"] + GROUPS["intero"]
EVAL_TAG = 31                     # world seed stream for diagnosis, distinct from training (tags 1-3)


def run_condition(state_dict, seed: int, wc: WorldConfig, n_envs: int, episodes: int,
                  p_erase: float, group: str | None, window: int, record: bool = False) -> Dict[str, object]:
    """Evaluate one agent in one condition. Same world seed for every condition of an agent."""
    torch.manual_seed(seed)
    agent = ErasureAgent(64, 1.0, 0.15)
    agent.load_state_dict(state_dict)
    agent.eval()
    world = NoEchoSwapWorld(n_envs, "M1", wc, np.random.SeedSequence([seed, EVAL_TAG, 17]))
    gen = torch.Generator().manual_seed(seed * 7919 + EVAL_TAG)
    rng = np.random.default_rng([seed, EVAL_TAG, 5])
    cols = GROUPS[group] if group else None
    correct = probes = 0
    in_band = steps = 0
    cells, targets, intero = [], [], []
    for _ in range(episodes):
        obs = world.reset()
        h = agent.init_state(n_envs)
        for t in range(wc.horizon):
            if cols is not None:
                hit = np.zeros(n_envs, dtype=bool)
                for k in range(window):
                    if t + k <= wc.horizon:
                        hit |= world.probe[t + k]
                if hit.any():
                    perm = rng.permutation(n_envs)
                    shuffled = obs[perm][:, cols]
                    obs[np.ix_(hit, cols)] = shuffled[hit]
            p = world.probe[t]
            if record and p.any():
                cells.append(world.y[p] * wc.grid + world.x[p])
                targets.append(world.target[t][p])
                intero.append(obs[p, GROUPS["intero"][0]])
            with torch.no_grad():
                hh = agent.core(torch.relu(agent.enc(torch.from_numpy(obs))), h)
                logits = agent.pi(hh)
                if p_erase > 0:
                    erase = torch.rand(n_envs, generator=gen) < p_erase
                    hh = hh * (~erase).to(hh.dtype)[:, None]
                h = hh
                a = torch.multinomial(torch.softmax(logits, -1), 1, generator=gen).squeeze(-1).numpy()
            obs, _, _ = world.step(a)
        s = world.stats
        correct += float(s["best_response"].sum())
        probes += float(s["probes"].sum())
        in_band += float(s["in_band"].sum())
        steps += n_envs * wc.horizon
    out: Dict[str, object] = {"acc": correct / max(probes, 1), "in_band": in_band / steps}
    if record:
        out["cells"] = np.concatenate(cells).tolist()
        out["targets"] = np.concatenate(targets).tolist()
        out["intero"] = np.concatenate(intero).tolist()
    return out


def cell_decoder_accuracy(cells, targets, grid: int) -> float:
    """Two-fold cross-validated accuracy of predicting the target from the agent's cell
    by the majority target of that cell in the other fold (ties and unseen cells: 0.5)."""
    cells, targets = np.asarray(cells), np.asarray(targets)
    folds = np.arange(cells.size) % 2
    score = 0.0
    for f in (0, 1):
        tr, te = folds != f, folds == f
        n1 = np.bincount(cells[tr], weights=targets[tr], minlength=grid * grid)
        n = np.bincount(cells[tr], minlength=grid * grid)
        frac = np.where(n > 0, n1 / np.maximum(n, 1), 0.5)
        pred = frac[cells[te]]
        right = np.where(pred == 0.5, 0.5, ((pred > 0.5).astype(int) == targets[te]).astype(float))
        score += right.sum()
    return float(score / cells.size)


def diagnose_agent(job) -> Dict[str, object]:
    """job = (label dict, state_dict bytes-free tensor dict, seed, wcd, n_envs, episodes, rate, window)."""
    label, sd, seed, wcd, n_envs, episodes, rate, window = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    out: Dict[str, object] = dict(label)
    out["intact"] = run_condition(sd, seed, wc, n_envs, episodes, 0.0, None, window)
    for name, p in (("full", rate), ("memoryless", 1.0)):
        base = run_condition(sd, seed, wc, n_envs, episodes, p, None, window, record=(name == "memoryless"))
        if name == "memoryless":
            t = np.asarray(base.pop("targets"))
            c = base.pop("cells")
            i = np.asarray(base.pop("intero"))
            base["cell_decoder"] = cell_decoder_accuracy(c, t, wc.grid)
            base["intero_by_target"] = [float(i[t == 0].mean()), float(i[t == 1].mean())]
        base["shuffled"] = {g: run_condition(sd, seed, wc, n_envs, episodes, p, g, window)["acc"] for g in GROUPS}
        out[name] = base
    out["seconds"] = round(time.time() - t0, 1)
    return out
