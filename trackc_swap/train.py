"""A2C training and evaluation for the swap cells.

A job is (objective, seed, kind): kind "pair" trains an S-FATE agent and its
S-YOKED partner in lockstep (the partner receives the donor's gain sequence at
the same iteration, step and env index); kind "nofate" trains one S-NOFATE
agent. The horizon end is a time-limit truncation: the return bootstraps from
the value of the final state. There is no in-world termination and no
operator stop anywhere in the code.
"""
from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Dict, Optional

import numpy as np
import torch

from .agent import Agent
from .env import SwapWorld, WorldConfig


@dataclass(frozen=True)
class TrainConfig:
    n_envs: int = 128
    rollout: int = 50
    iters: int = 1200
    hidden: int = 64
    lr: float = 1e-3
    gamma: float = 0.99
    lam: float = 0.95
    ent_coef: float = 0.01
    v_coef: float = 0.5
    grad_clip: float = 0.5
    kappa_f: float = 1.0
    s_core: float = 0.15
    eval_episodes: int = 2


class Runner:
    """One agent with its own world, optimizer and RNG streams."""

    def __init__(self, arm: str, objective: str, seed: int, wc: WorldConfig, tc: TrainConfig):
        self.arm, self.tc, self.wc = arm, tc, wc
        tag = {"FATE": 1, "YOKED": 2, "NOFATE": 3}[arm]
        self.world = SwapWorld(tc.n_envs, objective, wc, np.random.SeedSequence([seed, tag, 11]))
        torch.manual_seed(seed)                      # paired initialization within a seed
        self.agent = Agent(tc.hidden, tc.kappa_f, tc.s_core)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)

    def rollout(self, gains: Optional[np.ndarray], learn: bool, record_h: bool = False):
        """Run `rollout` steps. gains: None (own E decides), or an array [L, N]
        imposed from outside (yoked replay, zeros for no fate, ones for the
        imposed-noise control). Returns the gain sequence actually applied."""
        tc, w = self.tc, self.world
        logps, vals, ents, rews, used, hs = [], [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        for t in range(tc.rollout):
            g = w.gain() if gains is None else gains[t]
            used.append(np.asarray(g, dtype=np.float32))
            gt = torch.from_numpy(np.asarray(g, dtype=np.float32))
            with torch.set_grad_enabled(learn):
                logits, v, h = self.agent.step(obs, h, gt, self.gen)
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            nobs, r, done = w.step(idx.numpy())
            obs = torch.from_numpy(nobs)
            if learn:
                logps.append(dist.log_prob(idx)); vals.append(v); ents.append(dist.entropy())
                rews.append(torch.from_numpy(r.astype(np.float32)))
            if record_h:
                hs.append(h.detach().numpy().copy())
        if learn:
            with torch.no_grad():   # bootstrap from the value of the final state (truncation)
                g_next = w.gain() if gains is None else gains[-1]
                _, v_next, _ = self.agent.step(obs, h, torch.from_numpy(np.asarray(g_next, dtype=np.float32)), self.gen)
            vals_t = torch.stack(vals)
            adv = torch.zeros_like(vals_t)
            last = torch.zeros(tc.n_envs)
            nxt = v_next
            for t in reversed(range(tc.rollout)):
                delta = rews[t] + tc.gamma * nxt - vals_t[t].detach()
                last = delta + tc.gamma * tc.lam * last
                adv[t] = last
                nxt = vals_t[t].detach()
            ret = adv + vals_t.detach()
            a = (adv - adv.mean()) / (adv.std() + 1e-8)
            loss = (-(torch.stack(logps) * a).mean() + tc.v_coef * ((vals_t - ret) ** 2).mean()
                    - tc.ent_coef * torch.stack(ents).mean())
            self.opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.agent.parameters(), tc.grad_clip)
            self.opt.step()
        self.h, self.obs = h, obs
        return np.stack(used), (np.stack(hs) if record_h else None)

    def end_episode_if_due(self) -> Optional[Dict[str, float]]:
        """At the horizon: return the episode's statistics and start a new episode."""
        w = self.world
        if w.t < self.wc.horizon:
            return None
        out = summarize_stats(w.stats, self.tc.n_envs, self.wc.horizon)
        self.obs = torch.from_numpy(w.reset())
        self.h = self.agent.init_state(self.tc.n_envs)
        return out

    def evaluate(self, mode: str, donor_gains: Optional[np.ndarray] = None):
        """Fresh episodes, no learning. mode: own | zero | full | replay.
        Returns (mean statistics over episodes, applied gains [episodes*per_ep, L, N],
        mean per-unit hidden-state SD)."""
        tc, w, wc = self.tc, self.world, self.wc
        per_ep = wc.horizon // tc.rollout
        self.obs = torch.from_numpy(w.reset())
        self.h = self.agent.init_state(tc.n_envs)
        eps, applied, hs_all = [], [], []
        for ep in range(tc.eval_episodes):
            for i in range(per_ep):
                if mode == "own":
                    g = None
                elif mode == "replay":
                    g = donor_gains[ep * per_ep + i]
                else:
                    g = np.full((tc.rollout, tc.n_envs), 0.0 if mode == "zero" else 1.0, dtype=np.float32)
                used, hs = self.rollout(g, learn=False, record_h=True)
                applied.append(used)
                hs_all.append(hs.reshape(-1, tc.hidden))
            st = self.end_episode_if_due()
            st["mean_gain"] = float(np.mean(applied[-per_ep:]))
            eps.append(st)
        mean = {k: float(np.mean([e[k] for e in eps])) for k in eps[0]}
        h_sd = float(np.concatenate(hs_all).std(axis=0).mean())
        return mean, np.stack(applied), h_sd


def summarize_stats(stats: Dict[str, np.ndarray], n_envs: int, horizon: int) -> Dict[str, float]:
    eats, probes = stats["eats"].sum(), stats["probes"].sum()
    low = stats["steps_low"].sum()
    high = n_envs * horizon - low
    return {
        "rho": float(eats / n_envs) * (500.0 / horizon),          # consumed food per 500 steps
        "best_response_rate": float(stats["best_response"].sum() / max(probes, 1)),
        "report_rate": float(stats["reports"].sum() / max(probes, 1)),
        "in_band": float(stats["in_band"].sum() / (n_envs * horizon)),
        "eat_rate_low": float(stats["eats_low"].sum() / max(low, 1)),
        "eat_rate_high": float((eats - stats["eats_low"].sum()) / max(high, 1)),
    }


def run_job(job) -> Dict[str, object]:
    """job = (kind, objective, seed, world config dict, train config dict, doses).
    `doses` are the kappa_f values at which a no-fate agent is tested under
    imposed full noise; pair jobs train at tc.kappa_f."""
    kind, objective, seed, wcd, tcd, doses = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    assert (tc.iters * tc.rollout) % wc.horizon == 0 and wc.horizon % tc.rollout == 0
    t0 = time.time()
    out: Dict[str, object] = {"kind": kind, "objective": objective, "seed": seed, "kappa_f": tc.kappa_f}
    if kind == "pair":
        fate = Runner("FATE", objective, seed, wc, tc)
        yoked = Runner("YOKED", objective, seed, wc, tc)
        curves = {"FATE": [], "YOKED": []}
        for it in range(tc.iters):
            used, _ = fate.rollout(None, learn=True)
            yoked.rollout(used, learn=True)
            for name, r in (("FATE", fate), ("YOKED", yoked)):
                st = r.end_episode_if_due()
                if st is not None:
                    curves[name].append(st)
        ev_f, gains, hsd_f = fate.evaluate("own")
        ev_y, _, hsd_y = yoked.evaluate("replay", gains)
        out["S-FATE"] = {"eval": ev_f, "curve": curves["FATE"], "hidden_sd": hsd_f,
                         "eval_full_noise": fate.evaluate("full")[0],
                         "eval_zero_noise": fate.evaluate("zero")[0]}
        out["S-YOKED"] = {"eval": ev_y, "curve": curves["YOKED"], "hidden_sd": hsd_y,
                          "eval_zero_noise": yoked.evaluate("zero")[0]}
    elif kind == "nofate":
        r = Runner("NOFATE", objective, seed, wc, tc)
        zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
        curve = []
        for it in range(tc.iters):
            r.rollout(zeros, learn=True)
            st = r.end_episode_if_due()
            if st is not None:
                curve.append(st)
        ev, _, hsd = r.evaluate("zero")
        full = {}
        for dose in doses:                      # imposed full noise at each dose: task-load control
            r.agent.kappa_f = dose
            full[str(dose)] = r.evaluate("full")[0]
        out["S-NOFATE"] = {"eval": ev, "curve": curve, "hidden_sd": hsd, "eval_full_noise": full}
    else:
        raise ValueError(kind)
    out["seconds"] = round(time.time() - t0, 1)
    return out
