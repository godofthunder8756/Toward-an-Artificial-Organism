"""Track C swap, option P: how saved agents represent and use the body variable E (no training).

Additive module; every earlier module is unchanged. A saved agent is run with erasure off
(the carried state is never reset, so nothing is relocated and the SAT and GRADED worlds
coincide) in two conditions:

  intact   the agent's own observation;
  shuffled the interoceptive input (index 50) is permuted across environments at every step,
           which keeps its distribution and breaks its relation to the agent's own E.

In `intact`, at every step t >= WINDOW the agent's hidden state h_t (after reading
observation t) is recorded with:
  E_t        its true energy when observation t is made;
  D_t        E_t - E_{t-5}: the change interoception has not reported yet (it shows E_{t-5});
  intero_t   the interoceptive input itself;
  ate_t      whether it ate on the step before observation t (visible to it through the
             previous action and the previous reward).

Linear ridge decoders, two-fold cross-validated across environments, give R^2 for:
  h       -> E_t, D_t      (what the agent's state carries);
  raw     -> E_t           (intero_t alone: what the current input carries);
  window  -> E_t, D_t      (intero and ate over the last WINDOW steps: an ideal linear
                            readout of the recent inputs that matter for E).

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from .env import VIEW, WorldConfig
from .erasure import ErasureAgent, NoEchoSwapWorld
from .train import summarize_stats

INTERO = 2 * VIEW * VIEW          # index 50
WINDOW = 10                       # steps of input history in the window baseline
PROBE_TAG = 41                    # world seed stream for the probe, distinct from training (1-3) and diagnosis (31)
RIDGE = 1.0


def run_agent(state_dict, objective: str, seed: int, wc: WorldConfig, n_envs: int, episodes: int,
              shuffle_intero: bool, record: bool) -> Dict[str, object]:
    """Run one agent with erasure off. Same world seed in both conditions of an agent."""
    torch.manual_seed(seed)
    agent = ErasureAgent(64, 1.0, 0.15)
    agent.load_state_dict(state_dict)
    agent.eval()
    world = NoEchoSwapWorld(n_envs, objective, wc, np.random.SeedSequence([seed, PROBE_TAG, 17]))
    gen = torch.Generator().manual_seed(seed * 7919 + PROBE_TAG)
    rng = np.random.default_rng([seed, PROBE_TAG, 5])
    T = wc.horizon
    totals = None
    if record:
        H = np.zeros((episodes, T, n_envs, 64), dtype=np.float32)
        E = np.zeros((episodes, T, n_envs))
        D = np.zeros((episodes, T, n_envs))
        I = np.zeros((episodes, T, n_envs))
        A = np.zeros((episodes, T, n_envs))
    for ep in range(episodes):
        obs = world.reset()
        h = agent.init_state(n_envs)
        ate = np.zeros(n_envs)
        for t in range(T):
            if shuffle_intero:
                obs[:, INTERO] = obs[rng.permutation(n_envs), INTERO]
            with torch.no_grad():
                h = agent.core(torch.relu(agent.enc(torch.from_numpy(obs))), h)
                a = torch.multinomial(torch.softmax(agent.pi(h), -1), 1, generator=gen).squeeze(-1).numpy()
            if record:
                H[ep, t] = h.numpy()
                E[ep, t] = world.Ehist[t]
                D[ep, t] = world.Ehist[t] - world.Ehist[max(t - wc.intero_delay, 0)]
                I[ep, t] = obs[:, INTERO]
                A[ep, t] = ate
            before = world.stats["eats"].copy()
            obs, _, _ = world.step(a)
            ate = (world.stats["eats"] > before).astype(float)
        st = world.stats
        totals = {k: v.copy() for k, v in st.items()} if totals is None else {k: totals[k] + st[k] for k in st}
    out: Dict[str, object] = summarize_stats(totals, n_envs, T * episodes)
    out["eats"] = float(totals["eats"].sum())
    if record:
        out["_rec"] = (H, E, D, I, A)
    return out


def ridge_r2(X: np.ndarray, y: np.ndarray, env: np.ndarray, lam: float = RIDGE):
    """Two-fold (by environment parity) cross-validated ridge regression. Returns (R^2, MSE)."""
    X = X.reshape(len(y), -1).astype(np.float64)
    pred = np.empty_like(y, dtype=np.float64)
    folds = env % 2
    for f in (0, 1):
        tr, te = folds != f, folds == f
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-8
        Xt = (X[tr] - mu) / sd
        ym = y[tr].mean()
        w = np.linalg.solve(Xt.T @ Xt + lam * np.eye(X.shape[1]), Xt.T @ (y[tr] - ym))
        pred[te] = ((X[te] - mu) / sd) @ w + ym
    mse = float(np.mean((y - pred) ** 2))
    var = float(np.var(y))
    return (1.0 - mse / var if var > 0 else 0.0), mse


def decode(rec, window: int = WINDOW) -> Dict[str, float]:
    """R^2 of the h, raw and window decoders for E_t and D_t, over steps t >= window."""
    H, E, D, I, A = rec
    eps, T, n, _ = H.shape
    ts = np.arange(window, T)
    env = np.broadcast_to(np.arange(n), (eps, len(ts), n)).reshape(-1)
    Xh = H[:, ts].reshape(-1, H.shape[-1])
    y_e = E[:, ts].reshape(-1)
    y_d = D[:, ts].reshape(-1)
    raw = I[:, ts].reshape(-1, 1)
    win = np.concatenate([np.stack([I[:, ts - k] for k in range(window)], -1),
                          np.stack([A[:, ts - k] for k in range(window)], -1)], -1).reshape(-1, 2 * window)
    out = {}
    out["r2_E_h"], mse_e_h = ridge_r2(Xh, y_e, env)
    out["r2_E_raw"], mse_e_raw = ridge_r2(raw, y_e, env)
    out["r2_E_win"], _ = ridge_r2(win, y_e, env)
    out["r2_D_h"], _ = ridge_r2(Xh, y_d, env)
    out["r2_D_win"], _ = ridge_r2(win, y_d, env)
    out["gain_E"] = 1.0 - mse_e_h / mse_e_raw if mse_e_raw > 0 else 0.0
    out["E_sd"] = float(np.std(y_e))
    out["D_sd"] = float(np.std(y_d))
    return out


def probe_agent(job) -> Dict[str, object]:
    """job = (label dict, state dict, objective, seed, wcd, n_envs, episodes)."""
    label, sd, objective, seed, wcd, n_envs, episodes = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    out: Dict[str, object] = dict(label)
    intact = run_agent(sd, objective, seed, wc, n_envs, episodes, False, True)
    out.update(decode(intact.pop("_rec")))
    out["intact"] = intact
    out["shuffled"] = run_agent(sd, objective, seed, wc, n_envs, episodes, True, False)
    out["seconds"] = round(time.time() - t0, 1)
    return out
