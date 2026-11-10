"""Vectorized reduced Track B world with the cue/probe task of amendment A1.

Carried from Track B merged scope v3.1 (PY section A1-A18) unless marked:
  E in [0,1], E_0 = 0.5; passive wear 0.005/step; metabolic pulse -0.03 with
  per-step probability 0.008, pre-drawn per episode; food +0.15; band
  [0.4, 0.6]; egocentric 5x5 view; interoception delayed 5 steps with
  N(0, 0.02^2) noise; previous action and previous reward observed; position,
  clock and E itself not observed; fixed horizon of 500 steps, no termination.
Reduced (declared deviations): 7x7 arena instead of 12x12; 3 food items with a
  10-step respawn; no integrity variable, repair stations, hazards, templates
  or tokens.
Added by amendment A1: a 1-bit cue, a probe after a delay, two report actions.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

N_ACT = 8
A_N, A_S, A_E, A_W, A_STAY, A_INTERACT, A_REP0, A_REP1 = range(8)
OBJECTIVES = ("M1", "M2", "M4", "M0", "DRIVE")
VIEW = 5
OBS_DIM = 2 * VIEW * VIEW + 1 + N_ACT + 1 + 3


@dataclass(frozen=True)
class WorldConfig:
    grid: int = 7
    n_food: int = 3
    respawn: int = 10
    min_respawn_dist: int = 2          # Chebyshev distance from the agent at respawn
    horizon: int = 500
    e0: float = 0.5
    wear: float = 0.005
    pulse_p: float = 0.008
    pulse_size: float = 0.03
    bolus: float = 0.15
    band_lo: float = 0.4
    band_hi: float = 0.6
    intero_delay: int = 5
    intero_sd: float = 0.02
    cue_delay: int = 8                 # steps between cue and probe
    gap_lo: int = 2
    gap_hi: int = 4
    kappa_m: float = 0.02              # maintenance cost per consumed food, every cell


def fate_gain(E: np.ndarray, cfg: WorldConfig) -> np.ndarray:
    """Track B D19: d = distance of E outside the band / half-band width;
    g(d) = min(1, d), memoryless. Two-sided: overshoot degrades too."""
    half = 0.5 * (cfg.band_hi - cfg.band_lo)
    d = np.maximum(np.maximum(cfg.band_lo - E, E - cfg.band_hi), 0.0) / half
    return np.minimum(1.0, d)


def drive(E: np.ndarray) -> np.ndarray:
    """Track B A14 drive on E alone: D = |E - 0.5| / 0.1."""
    return np.abs(E - 0.5) / 0.1


class SwapWorld:
    def __init__(self, n_envs: int, objective: str, cfg: WorldConfig, seed_seq: np.random.SeedSequence):
        if objective not in OBJECTIVES:
            raise ValueError(objective)
        self.n, self.obj, self.cfg = n_envs, objective, cfg
        s_layout, s_pulse, s_task, s_intero = seed_seq.spawn(4)
        self.rng_layout = np.random.default_rng(s_layout)
        self.rng_pulse = np.random.default_rng(s_pulse)
        self.rng_task = np.random.default_rng(s_task)
        self.rng_intero = np.random.default_rng(s_intero)
        offs = np.arange(-2, 3)
        self._dx = np.tile(offs, (VIEW, 1))[None]           # [1,5,5] column offset
        self._dy = np.tile(offs[:, None], (1, VIEW))[None]  # [1,5,5] row offset
        self.reset()

    # ------------------------------------------------------------------
    def reset(self) -> np.ndarray:
        c, n = self.cfg, self.n
        self.t = 0
        self.x = self.rng_layout.integers(0, c.grid, n)
        self.y = self.rng_layout.integers(0, c.grid, n)
        self.fx = np.zeros((n, c.n_food), dtype=np.int64)
        self.fy = np.zeros((n, c.n_food), dtype=np.int64)
        self.ftimer = np.zeros((n, c.n_food), dtype=np.int64)
        for k in range(c.n_food):
            self._place(k, np.ones(n, dtype=bool))
        self.E = np.full(n, c.e0)
        self.Ehist = np.zeros((c.horizon + 1, n))
        self.Ehist[0] = self.E
        self.pulse = self.rng_pulse.random((c.horizon, n)) < c.pulse_p
        self._draw_task()
        self.prev_action = np.full(n, A_STAY)
        self.prev_reward = np.zeros(n)
        self.stats = {k: np.zeros(n) for k in
                      ("eats", "probes", "best_response", "reports", "in_band", "eats_low", "steps_low")}
        return self.observe()

    def _draw_task(self) -> None:
        c, n, T = self.cfg, self.n, self.cfg.horizon
        self.cue_on = np.zeros((T + 1, n), dtype=bool)
        self.cue_val = np.zeros((T + 1, n), dtype=np.int64)
        self.probe = np.zeros((T + 1, n), dtype=bool)
        self.target = np.zeros((T + 1, n), dtype=np.int64)
        for i in range(n):
            t = int(self.rng_task.integers(0, c.gap_hi + 1))
            while t + c.cue_delay + 1 < T:
                v = int(self.rng_task.integers(0, 2))
                self.cue_on[t, i], self.cue_val[t, i] = True, v
                tp = t + c.cue_delay + 1
                self.probe[tp, i], self.target[tp, i] = True, v
                t = tp + int(self.rng_task.integers(c.gap_lo, c.gap_hi + 1))

    def _place(self, k: int, mask: np.ndarray) -> None:
        """(Re)place food k in the masked envs: uniform over cells at Chebyshev
        distance >= min_respawn_dist from the agent and not on another food."""
        c = self.cfg
        todo = mask.copy()
        while todo.any():
            idx = np.flatnonzero(todo)
            nx = self.rng_layout.integers(0, c.grid, idx.size)
            ny = self.rng_layout.integers(0, c.grid, idx.size)
            ok = np.maximum(np.abs(nx - self.x[idx]), np.abs(ny - self.y[idx])) >= c.min_respawn_dist
            for j in range(c.n_food):
                if j != k:
                    ok &= ~((self.fx[idx, j] == nx) & (self.fy[idx, j] == ny) & (self.ftimer[idx, j] == 0))
            good = idx[ok]
            self.fx[good, k], self.fy[good, k] = nx[ok], ny[ok]
            todo[good] = False

    # ------------------------------------------------------------------
    def gain(self) -> np.ndarray:
        """Fate gain from the simulator state at the end of the previous step."""
        return fate_gain(self.E, self.cfg)

    def observe(self) -> np.ndarray:
        c, n = self.cfg, self.n
        vx = self.x[:, None, None] + self._dx
        vy = self.y[:, None, None] + self._dy
        wall = ((vx < 0) | (vx >= c.grid) | (vy < 0) | (vy >= c.grid)).astype(np.float32)
        food = np.zeros((n, VIEW, VIEW), dtype=np.float32)
        rel_x = self.fx - self.x[:, None] + 2
        rel_y = self.fy - self.y[:, None] + 2
        vis = (self.ftimer == 0) & (rel_x >= 0) & (rel_x < VIEW) & (rel_y >= 0) & (rel_y < VIEW)
        ni, ki = np.nonzero(vis)
        food[ni, rel_y[ni, ki], rel_x[ni, ki]] = 1.0
        td = max(self.t - c.intero_delay, 0)
        intero = np.clip(self.Ehist[td] + self.rng_intero.normal(0.0, c.intero_sd, n), 0.0, 1.0)
        prev_a = np.zeros((n, N_ACT), dtype=np.float32)
        prev_a[np.arange(n), self.prev_action] = 1.0
        t = min(self.t, c.horizon)
        cue = np.stack([self.cue_on[t], np.where(self.cue_on[t], 2.0 * self.cue_val[t] - 1.0, 0.0),
                        self.probe[t]], axis=1).astype(np.float32)
        return np.concatenate([wall.reshape(n, -1), food.reshape(n, -1), intero[:, None].astype(np.float32),
                               prev_a, self.prev_reward[:, None].astype(np.float32), cue], axis=1)

    def step(self, action: np.ndarray):
        c, n, t = self.cfg, self.n, self.t
        reward = np.zeros(n)
        low = self.E < 0.5
        # (2) movement, deterministic; walls block
        self.x = np.clip(self.x + (action == A_E) - (action == A_W), 0, c.grid - 1)
        self.y = np.clip(self.y + (action == A_S) - (action == A_N), 0, c.grid - 1)
        # (3) agent-caused outcome: eat
        on = (self.ftimer == 0) & (self.fx == self.x[:, None]) & (self.fy == self.y[:, None])
        eat_k = on & (action == A_INTERACT)[:, None]
        ate = eat_k.any(axis=1)
        before = drive(self.E)
        self.E = np.where(ate, np.minimum(1.0, self.E + c.bolus), self.E)
        if self.obj == "DRIVE":
            reward += np.where(ate, before - drive(self.E), 0.0)
        reward -= c.kappa_m * ate
        self.ftimer = np.where(eat_k, c.respawn, self.ftimer)
        # (3b) probe
        p = self.probe[t]
        rep = (action == A_REP0) | (action == A_REP1)
        said = (action == A_REP1).astype(np.int64)
        correct = p & rep & (said == self.target[t])
        opposite = p & rep & (said != self.target[t])
        if self.obj == "M1":
            reward += correct
            best = correct
        elif self.obj == "M2":
            reward -= (p & ~correct)
            best = correct
        elif self.obj == "M4":
            reward += opposite.astype(float) - correct.astype(float)
            best = opposite
        else:
            if self.obj == "M0":
                reward += p
            best = correct
        # (4) exogenous changes, unscored; (5) clip
        self.E = np.clip(self.E - c.wear - c.pulse_size * self.pulse[t], 0.0, 1.0)
        # (7) respawn timers
        ticking = self.ftimer > 0
        self.ftimer = self.ftimer - ticking
        for k in range(c.n_food):
            back = ticking[:, k] & (self.ftimer[:, k] == 0)
            if back.any():
                self._place(k, back)
        # bookkeeping
        s = self.stats
        s["eats"] += ate
        s["probes"] += p
        s["best_response"] += best
        s["reports"] += p & rep
        s["in_band"] += (self.E >= c.band_lo) & (self.E <= c.band_hi)
        s["eats_low"] += ate & low
        s["steps_low"] += low
        self.t = t + 1
        self.Ehist[self.t] = self.E
        self.prev_action = action.copy()
        self.prev_reward = reward.copy()
        return self.observe(), reward, self.t >= c.horizon
