"""Track C swap, option W: what the hidden state of stored two-variable agents carries after a meal.

Additive module; every earlier module is unchanged. No training. Options G and G2 found that in
the two-variable cell (B2) derived regulators hold back after a meal more specifically to the
variable that was fed than paid regulators do. This module asks whether the recurrent state
itself carries which kind of item was just eaten, beyond what the agent's inputs show.

A stored agent is run exactly as option G's downstream probe runs it (general.run_probe_g: the
same world seed, streams and action sampling, so the same trajectory, with erasure off), and at
every step t the state h_t that the policy reads is recorded together with:
  the observation o_t, without the zeroed echo of the previous action and reward;
  both interoceptive readings over the previous nine steps;
  the steps since the last meal of each variable.

Samples:
  kind      steps with s_k = steps since the last meal of variable k in 1..10, and the other
            variable's last meal at least 10 steps before that meal (s_other >= s_k + 10);
            label k. A meal on the step before o_t has s_k = 1.
  meal      "post" steps as `kind` with s_k in 2..5 against "control" steps with no meal of
            either variable in the last 10 steps (both s >= 11), the control steps subsampled
            (seeded) to the number of post steps.

Decoders: L2-regularised logistic regression on standardised features, fitted by Newton's
method, two-fold cross-validated across environments (by environment parity, as option P's
ridge decoders). The baseline B is o_t plus the reading history: everything the agent can see
now and has recently seen of its body, but not the meal itself (the eaten item is gone from
the view, and the delayed readings do not yet show it for s <= 5). The state measure is the
cross-validated log-likelihood gain, in bits per sample, of the decoder from [h_t, B] over the
decoder from B alone: what h_t adds about the label beyond the inputs.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict, List, Optional

import numpy as np
import torch

from .causal import CAUSAL_TAG
from .env import N_ACT, VIEW, WorldConfig
from .general import INTERO2, OBS_DIM2, TwoBodyWorld, WideAgent, summarize2

CELL = VIEW * VIEW
ECHO = (3 * CELL + 2, 3 * CELL + 2 + N_ACT + 1)     # the zeroed echo columns of a B2 observation
OBS_KEEP = np.r_[0:ECHO[0], ECHO[1]:OBS_DIM2]        # baseline columns of o_t
HIST = 9                                             # previous steps of the readings in the baseline
MAX_SINCE = 10                                       # kind samples: steps since the meal, 1..MAX_SINCE
POST = (2, 5)                                        # the post-meal steps of options Q-G2
CLEAN = 10                                           # the other kind's last meal at least this much earlier
CTRL_MIN = 11                                        # meal samples: control steps, no meal in the last 10
LAM = 1.0                                            # L2 penalty on standardised weights (option P's RIDGE)
MIN_SAMPLES = 1000                                   # samples needed per class for a measure


def probe_record(state_dict, hidden: int, rate: float, seed: int, wc: WorldConfig, n_envs: int,
                 episodes: int) -> Dict[str, object]:
    """Run one stored B2 agent as general.run_probe_g does (same trajectory) and record the samples."""
    torch.manual_seed(seed)
    agent = WideAgent(hidden, rate, 0.15, OBS_DIM2)
    world = TwoBodyWorld(n_envs, "M1", wc, np.random.SeedSequence([seed, CAUSAL_TAG, 17]))
    agent.load_state_dict(state_dict)
    agent.eval()
    gen = torch.Generator().manual_seed(seed * 7919 + CAUSAL_TAG)
    T = wc.horizon
    totals = None
    keep = {k: [] for k in ("h", "b", "since", "env")}
    for _ in range(episodes):
        obs = world.reset()
        h = agent.init_state(n_envs)
        since = np.full((2, n_envs), 10 ** 6)
        hist = np.tile(obs[:, INTERO2[0]:INTERO2[1] + 1], (HIST, 1, 1))  # [HIST, n, 2], oldest first
        for t in range(T):
            with torch.no_grad():
                hh = agent.core(torch.relu(agent.enc(torch.from_numpy(obs))), h)
                probs = torch.softmax(agent.pi(hh), -1)
                a = torch.multinomial(probs, 1, generator=gen).squeeze(-1).numpy()
            s_min = since.min(axis=0)
            take = (s_min <= MAX_SINCE) | (s_min >= CTRL_MIN)
            if t >= HIST and take.any():
                idx = np.flatnonzero(take)
                keep["h"].append(hh.numpy()[idx])
                keep["b"].append(np.concatenate([obs[idx][:, OBS_KEEP], hist[:, idx].transpose(1, 0, 2).reshape(len(idx), -1)], 1))
                keep["since"].append(since[:, idx].T.copy())
                keep["env"].append(idx)
            h = hh
            hist = np.concatenate([hist[1:], obs[None, :, INTERO2[0]:INTERO2[1] + 1]], 0)
            before = world.stats["eats_r"].copy()
            obs, _, _ = world.step(a)
            since = np.where(world.stats["eats_r"] > before, 1, since + 1)
        st = world.stats
        totals = {k: v.copy() for k, v in st.items()} if totals is None else {k: totals[k] + st[k] for k in st}
    out: Dict[str, object] = summarize2(totals, n_envs, T * episodes)
    out["eats"] = float(totals["eats"].sum())
    out["_rec"] = {k: np.concatenate(v) for k, v in keep.items()}
    return out


def kind_samples(rec, s_lo: int, s_hi: int):
    """(rows, label) of `kind` samples with s_k in s_lo..s_hi."""
    s = rec["since"]
    lab = np.argmin(s, axis=1)
    sk, so = s.min(axis=1), s.max(axis=1)
    rows = np.flatnonzero((sk >= s_lo) & (sk <= s_hi) & (so >= sk + CLEAN))
    return rows, lab[rows]


def meal_samples(rec, seed: int):
    """(rows, label) of `meal` samples: post (1) against an equal-sized seeded subsample of control (0)."""
    post, _ = kind_samples(rec, *POST)
    ctrl = np.flatnonzero(rec["since"].min(axis=1) >= CTRL_MIN)
    rng = np.random.default_rng([seed, 97])
    if len(ctrl) > len(post):
        ctrl = np.sort(rng.choice(ctrl, len(post), replace=False))
    rows = np.concatenate([post, ctrl])
    return rows, np.concatenate([np.ones(len(post), int), np.zeros(len(ctrl), int)])


def _fit(X: np.ndarray, y: np.ndarray, lam: float, iters: int = 30) -> np.ndarray:
    """L2 logistic regression by Newton's method; X carries an intercept column (not penalised)."""
    w = np.zeros(X.shape[1])
    pen = np.full(X.shape[1], lam)
    pen[-1] = 0.0
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(X @ w, -30, 30)))
        g = X.T @ (p - y) + pen * w
        Hm = (X * (p * (1 - p))[:, None]).T @ X + np.diag(pen + 1e-9)
        step = np.linalg.solve(Hm, g)
        w -= step
        if np.max(np.abs(step)) < 1e-7:
            break
    return w


def cv_logistic(X: np.ndarray, y: np.ndarray, env: np.ndarray, lam: float = LAM):
    """Two-fold (environment parity) cross-validated logistic regression.
    Returns (log-likelihood in bits summed over all samples, balanced accuracy)."""
    X = X.astype(np.float64)
    p = np.empty(len(y))
    for f in (0, 1):
        tr, te = (env % 2) != f, (env % 2) == f
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-8
        Xt = np.c_[(X[tr] - mu) / sd, np.ones(tr.sum())]
        w = _fit(Xt, y[tr].astype(np.float64), lam)
        p[te] = 1.0 / (1.0 + np.exp(-np.clip(np.c_[(X[te] - mu) / sd, np.ones(te.sum())] @ w, -30, 30)))
    p = np.clip(p, 1e-6, 1 - 1e-6)
    ll = float(np.sum(y * np.log2(p) + (1 - y) * np.log2(1 - p)))
    pred = p >= 0.5
    bacc = 0.5 * (np.mean(pred[y == 1]) + np.mean(~pred[y == 0]))
    return ll, float(bacc)


def gain(rec, rows, y, lam: float = LAM) -> Optional[Dict[str, float]]:
    """What h adds about y beyond the baseline: bits per sample, with each decoder's balanced accuracy.
    None with fewer than MIN_SAMPLES samples of either class, or samples in only one fold."""
    if min(np.sum(y == 0), np.sum(y == 1)) < MIN_SAMPLES or len(set(rec["env"][rows] % 2)) < 2:
        return None
    env = rec["env"][rows]
    H, B = rec["h"][rows], rec["b"][rows]
    ll_b, acc_b = cv_logistic(B, y, env, lam)
    ll_hb, acc_hb = cv_logistic(np.c_[H, B], y, env, lam)
    ll_h, acc_h = cv_logistic(H, y, env, lam)
    q = float(np.mean(y))
    ent = -(q * np.log2(q) + (1 - q) * np.log2(1 - q))
    n = len(y)
    return {"n": int(n), "n1": int(np.sum(y == 1)), "entropy": ent, "bits": (ll_hb - ll_b) / n,
            "bits_baseline": ent + ll_b / n, "bits_h_alone": ent + ll_h / n,
            "acc_baseline": acc_b, "acc_h_alone": acc_h, "acc_both": acc_hb}


def decode_agent(rec, seed: int) -> Dict[str, object]:
    """All measures of one agent. `kind` is the primary (s_k in 2..5)."""
    out: Dict[str, object] = {}
    rows, y = kind_samples(rec, *POST)
    out["kind"] = gain(rec, rows, y)
    out["kind_lam"] = {str(l): (g["bits"] if (g := gain(rec, rows, y, l)) else None) for l in (10.0, 100.0)}
    out["kind_by_step"] = {}
    for s in range(1, MAX_SINCE + 1):
        r, yy = kind_samples(rec, s, s)
        g = gain(rec, r, yy)
        out["kind_by_step"][str(s)] = None if g is None else {k: g[k] for k in ("n", "bits", "acc_h_alone", "acc_baseline")}
    r, yy = meal_samples(rec, seed)
    out["meal"] = gain(rec, r, yy)
    return out


def run_agent_w(job) -> Dict[str, object]:
    """job = (label dict, state dict, hidden, seed, rate, wcd, n_envs, episodes)."""
    label, sd, hidden, seed, rate, wcd, n_envs, episodes = job
    torch.set_num_threads(1)
    t0 = time.time()
    run = probe_record(sd, hidden, rate, seed, WorldConfig(**wcd), n_envs, episodes)
    rec = run.pop("_rec")
    out = dict(label) | {"base": run} | decode_agent(rec, seed)
    out["seconds"] = round(time.time() - t0, 1)
    return out
