"""Track C swap, option Q: causal probes of how saved regulators use E (no training).

Additive module; every earlier module is unchanged. A saved agent is run in the v7/v8
world (echo-free, erasure also relocates) in one of three erasure modes:

  off        the carried state is never erased (as in option P);
  own        the agent's trained fate: erased with probability rate * gain(E), its own E
             deciding, with relocation on erasure (as in training and scoring);
  scrambled  the same erasure draws, but the mask is permuted across environments at every
             step. The number of erasures and relocations is kept; their relation to the
             agent's own E is broken.

Optionally the interoceptive input (index 50) is permuted across environments at every
step, as in option P.

Eat-propensity probe (mode off only; a side computation that does not change the run).
At every step the policy's probability of INTERACT is computed for the current
observation with food placed at the agent's own cell (the centre of the food view),
  psi_carried  from the agent's carried state;
  psi_zero     from a zeroed (erased) state.
It answers "how ready is the agent to eat right now, if it stood on food". Recorded with
it: interoception, true E, and the number of steps since the agent last ate.

For five steps after a meal the interoceptive input still reports E from before the
meal. A drop in psi_carried over those steps, against steps with the same interoceptive
reading and no recent meal, can only come from the carried state: the agent uses what it
remembers of its own eating.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from .env import A_INTERACT, VIEW, WorldConfig
from .erasure import ErasureAgent
from .relocate import RelocGradedWorld, RelocSwapWorld
from .train import summarize_stats

INTERO = 2 * VIEW * VIEW                       # index 50
FOOD_HERE = VIEW * VIEW + (VIEW // 2) * VIEW + VIEW // 2   # food at the agent's own cell: index 37
CAUSAL_TAG = 43                                # world seed stream, distinct from 1-3, 31 and 41
MODES = ("off", "own", "scrambled")
BINS = (0.0, 0.35, 0.40, 0.45, 0.50)           # interoceptive reading, for matching post-meal and control steps
POST = (2, 5)                                  # steps since the meal counted as "post-meal" (inclusive)
CTRL_MIN = 11                                  # control steps: no meal in the last 10 steps
MIN_BIN = 20                                   # samples needed in a bin, in both sets
MIN_POST = 100                                 # post-meal samples needed overall


def run_mode(state_dict, objective: str, gain_rule: str, rate: float, seed: int, wc: WorldConfig,
             n_envs: int, episodes: int, mode: str, shuffle_intero: bool = False,
             probe: bool = False) -> Dict[str, object]:
    """Run one agent in one erasure mode. Same world seed for every condition of an agent."""
    if mode not in MODES:
        raise ValueError(mode)
    torch.manual_seed(seed)
    agent = ErasureAgent(64, rate, 0.15)
    agent.load_state_dict(state_dict)
    agent.eval()
    cls = RelocGradedWorld if gain_rule == "GRADED" else RelocSwapWorld
    world = cls(n_envs, objective, wc, np.random.SeedSequence([seed, CAUSAL_TAG, 17]))
    gen = torch.Generator().manual_seed(seed * 7919 + CAUSAL_TAG)
    rng = np.random.default_rng([seed, CAUSAL_TAG, 5])
    T = wc.horizon
    totals, erasures = None, 0
    rec = {k: [] for k in ("psi", "psi0", "intero", "E", "since")} if probe else None
    for _ in range(episodes):
        obs = world.reset()
        h = agent.init_state(n_envs)
        since = np.full(n_envs, 10 ** 6)                      # steps since the last meal
        for t in range(T):
            if shuffle_intero:
                obs[:, INTERO] = obs[rng.permutation(n_envs), INTERO]
            g = world.gain()
            with torch.no_grad():
                x = torch.from_numpy(obs)
                if probe:
                    star = x.clone()
                    star[:, FOOD_HERE] = 1.0
                    z = torch.relu(agent.enc(star))
                    rec["psi"].append(torch.softmax(agent.pi(agent.core(z, h)), -1)[:, A_INTERACT].numpy())
                    rec["psi0"].append(torch.softmax(agent.pi(agent.core(z, torch.zeros_like(h))), -1)
                                       [:, A_INTERACT].numpy())
                    rec["intero"].append(obs[:, INTERO].copy())
                    rec["E"].append(world.E.copy())
                    rec["since"].append(since.copy())
                hh = agent.core(torch.relu(agent.enc(x)), h)
                logits = agent.pi(hh)
                if mode != "off":
                    p = torch.clamp(rate * torch.from_numpy(np.asarray(g, dtype=np.float32)), 0.0, 1.0)
                    erase = (torch.rand(p.shape, generator=gen) < p).numpy()
                    if mode == "scrambled":
                        erase = erase[rng.permutation(n_envs)]
                    erasures += int(erase.sum())
                    hh = hh * torch.from_numpy(~erase).to(hh.dtype)[:, None]
                    world.relocate_next = erase.copy()
                a = torch.multinomial(torch.softmax(logits, -1), 1, generator=gen).squeeze(-1).numpy()
                h = hh
            before = world.stats["eats"].copy()
            obs, _, _ = world.step(a)
            ate = world.stats["eats"] > before
            since = np.where(ate, 1, since + 1)
        st = world.stats
        totals = {k: v.copy() for k, v in st.items()} if totals is None else {k: totals[k] + st[k] for k in st}
    out: Dict[str, object] = summarize_stats(totals, n_envs, T * episodes)
    out["eats"] = float(totals["eats"].sum())
    out["erasures"] = erasures
    if probe:
        out["_rec"] = {k: np.concatenate(v) for k, v in rec.items()}
    return out


def suppression(rec) -> Dict[str, object]:
    """Post-meal suppression of eat propensity, matched on the interoceptive reading.

    post: steps 2-5 after a meal (interoception has not reported it) with reading < 0.5;
    ctrl: steps with reading < 0.5 and no meal in the last 10 steps.
    S = 1 - sum_b n_post_b * mean_post_b / sum_b n_post_b * mean_ctrl_b over bins of the reading
    with at least MIN_BIN samples in both sets. None if fewer than MIN_POST post samples remain."""
    psi, intero, since = rec["psi"], rec["intero"], rec["since"]
    post = (since >= POST[0]) & (since <= POST[1])
    ctrl = since >= CTRL_MIN
    num = den = 0.0
    n_used = 0
    per_bin = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        b = (intero >= lo) & (intero < hi)
        npost, nctrl = int((b & post).sum()), int((b & ctrl).sum())
        if npost >= MIN_BIN and nctrl >= MIN_BIN:
            mp, mc = float(psi[b & post].mean()), float(psi[b & ctrl].mean())
            num += npost * mp
            den += npost * mc
            n_used += npost
            per_bin.append({"lo": lo, "hi": hi, "n_post": npost, "n_ctrl": nctrl, "psi_post": mp, "psi_ctrl": mc,
                            "S": 1.0 - mp / mc if mc > 0 else None})
        else:
            per_bin.append({"lo": lo, "hi": hi, "n_post": npost, "n_ctrl": nctrl, "psi_post": None,
                            "psi_ctrl": None, "S": None})
    S = (1.0 - num / den) if (n_used >= MIN_POST and den > 0) else None
    return {"S": S, "n_post": n_used, "per_bin": per_bin}


def zero_state_ratio(rec) -> Dict[str, object]:
    """Eat propensity from a zeroed state against the carried state, on steps where the
    interoceptive reading is in band (0.45-0.55) and no meal happened in the last 10 steps."""
    m = (rec["intero"] >= 0.45) & (rec["intero"] < 0.55) & (rec["since"] >= CTRL_MIN)
    if m.sum() < MIN_POST:
        return {"n": int(m.sum()), "psi_zero": None, "psi_carried": None}
    return {"n": int(m.sum()), "psi_zero": float(rec["psi0"][m].mean()), "psi_carried": float(rec["psi"][m].mean())}


def causal_agent(job) -> Dict[str, object]:
    """job = (label dict, state dict, objective, gain_rule, rate, seed, wcd, n_envs, episodes, full).
    full: also run own, own with shuffled interoception, and scrambled (fate agents only)."""
    label, sd, objective, gain_rule, rate, seed, wcd, n_envs, episodes, full = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    out: Dict[str, object] = dict(label)
    off = run_mode(sd, objective, gain_rule, rate, seed, wc, n_envs, episodes, "off", probe=True)
    rec = off.pop("_rec")
    out["suppression"] = suppression(rec)
    out["zero_state"] = zero_state_ratio(rec)
    out["off"] = off
    if full:
        out["own"] = run_mode(sd, objective, gain_rule, rate, seed, wc, n_envs, episodes, "own")
        out["own_shuffled"] = run_mode(sd, objective, gain_rule, rate, seed, wc, n_envs, episodes, "own",
                                       shuffle_intero=True)
        out["scrambled"] = run_mode(sd, objective, gain_rule, rate, seed, wc, n_envs, episodes, "scrambled")
    out["seconds"] = round(time.time() - t0, 1)
    return out
