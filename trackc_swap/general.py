"""Track C swap, generality: the derived/paid comparison of options R-R4 in two new cells.

Additive module; every earlier module is unchanged. Options R to R4 found, in one cell (the
v7/v8 world, a 64-unit recurrent core), that derived regulators hold back from getting another
meal after a meal they have not yet sensed far more than paid regulators matched for regulation
(the combined index K). This module runs the same three arms in two cells that each change one
thing:

  H128  the same world and arms, with a 128-unit recurrent core. Nothing else changes; the
        arms are option R's classes with `hidden` set.
  B2    a world with two body variables, a 64-unit core. Each variable (index 0 "energy",
        index 1 "water") has its own items on the grid, its own delayed interoceptive
        channel, its own wear and pulses, and the same band. INTERACT consumes whatever item
        is under the agent and raises that item's variable. The fate gain is the larger of
        the two variables' SAT gains, so memory is erased when either variable is out of
        band. The payment is the same weight times that same gain.

Arms in both cells (option R's):
  DERIVED  its own body state decides its erasure; task reward only;
  YOKED    replays the derived agent's erasure gains; task reward only;
  PAID     replays the same gains; task reward minus `pay` times the gain of its own body state.

The post-meal probes of options Q and R2 are generalized to any core size and to one probe per
body variable; with 64 units and one variable they reproduce paid2.run_probe2 exactly. The
decoding measures of option P (the anticipation index) are not taken: over R2, R3 and R4 they
did not separate the arms.

Every agent loads its own deep copy of the phase-1 state (TRACKC_SWAP_ERRATUM_1.md).
Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict, List, Optional

import numpy as np
import torch
import torch.nn as nn

from .causal import CAUSAL_TAG, CTRL_MIN, FOOD_HERE, INTERO, suppression
from .env import A_E, A_INTERACT, A_N, A_REP0, A_REP1, A_S, A_W, N_ACT, VIEW, SwapWorld, WorldConfig, fate_gain
from .erasure import ErasureAgent
from .factorial import _train, state_from_bytes, state_to_bytes
from .paid import ArmRunner, _evaluate, _lockstep, load_independent
from .paid2 import approach_mass, approach_suppression, flat_readiness
from .relocate import RelocAgent, RelocSwapWorld, run_phase1_reloc
from .train import TrainConfig, summarize_stats

CELLS = {"BASE": {"hidden": 64, "n_res": 1},       # options R-R4's cell; used by the tests only
         "H128": {"hidden": 128, "n_res": 1},
         "B2": {"hidden": 64, "n_res": 2}}
N_RES = 2
CELL = VIEW * VIEW                                 # cells in a view
OBS_DIM2 = 3 * CELL + N_RES + N_ACT + 1 + 3        # wall, two item views, two readings, zeroed echo, cue
ITEM_VIEW = (CELL, 2 * CELL)                       # start of each variable's item view
INTERO2 = (3 * CELL, 3 * CELL + 1)                 # index of each variable's interoceptive reading
CENTRE = (VIEW // 2) * VIEW + VIEW // 2            # the agent's own cell within a view
G_TAGS = {"FATE": 1, "YOKED": 2, "NOFATE": 3, "PAID": 4}   # option R's stream tags


class TwoBodyWorld:
    """The v7/v8 world (echo-free; an erasure also relocates the agent) with two body variables.

    Items 0..n_food-1 belong to variable 0 and n_food..2*n_food-1 to variable 1; no two active
    items share a cell. Each variable follows env.SwapWorld's rules for E with its own pulse
    and interoception streams. `pay` > 0 adds the evaluator's penalty of option R ("gain"
    kind): pay times the fate gain of the state after the step."""
    pay = 0.0

    def __init__(self, n_envs: int, objective: str, cfg: WorldConfig, seed_seq: np.random.SeedSequence):
        if objective != "M1":
            raise ValueError(objective)
        self.n, self.obj, self.cfg = n_envs, objective, cfg
        s = seed_seq.spawn(4 + 2 * N_RES)
        self.rng_layout, self.rng_task, self.rng_relocate = (np.random.default_rng(x) for x in s[:3])
        self.rng_pulse = [np.random.default_rng(x) for x in s[3:3 + N_RES]]
        self.rng_intero = [np.random.default_rng(x) for x in s[3 + N_RES:3 + 2 * N_RES]]
        self.kind = np.repeat(np.arange(N_RES), cfg.n_food)             # variable of each item
        offs = np.arange(-2, 3)
        self._dx = np.tile(offs, (VIEW, 1))[None]
        self._dy = np.tile(offs[:, None], (1, VIEW))[None]
        self.relocate_next: Optional[np.ndarray] = None
        self.relocations = 0
        self.reset()

    _draw_task = SwapWorld._draw_task                # the cue/probe schedule, unchanged

    def reset(self) -> np.ndarray:
        c, n, K = self.cfg, self.n, len(self.kind)
        self.t = 0
        self.relocate_next = None
        self.x = self.rng_layout.integers(0, c.grid, n)
        self.y = self.rng_layout.integers(0, c.grid, n)
        self.fx = np.zeros((n, K), dtype=np.int64)
        self.fy = np.zeros((n, K), dtype=np.int64)
        self.ftimer = np.ones((n, K), dtype=np.int64)                   # inactive until placed
        for k in range(K):
            self._place(k, np.ones(n, dtype=bool))
            self.ftimer[:, k] = 0
        self.B = np.full((N_RES, n), c.e0)
        self.Bhist = np.zeros((c.horizon + 1, N_RES, n))
        self.Bhist[0] = self.B
        self.pulse = np.stack([g.random((c.horizon, n)) < c.pulse_p for g in self.rng_pulse])   # [2, T, n]
        self._draw_task()
        z = lambda *shape: np.zeros(shape)
        self.stats = {"eats": z(n), "probes": z(n), "best_response": z(n), "reports": z(n), "in_band": z(n),
                      "in_band_r": z(N_RES, n), "eats_r": z(N_RES, n), "eats_low_r": z(N_RES, n),
                      "steps_low_r": z(N_RES, n)}
        return self.observe()

    def _place(self, k: int, mask: np.ndarray) -> None:
        """(Re)place item k in the masked envs: uniform over cells at Chebyshev distance
        >= min_respawn_dist from the agent and not on another active item of either kind."""
        c = self.cfg
        todo = mask.copy()
        while todo.any():
            idx = np.flatnonzero(todo)
            nx = self.rng_layout.integers(0, c.grid, idx.size)
            ny = self.rng_layout.integers(0, c.grid, idx.size)
            ok = np.maximum(np.abs(nx - self.x[idx]), np.abs(ny - self.y[idx])) >= c.min_respawn_dist
            for j in range(len(self.kind)):
                if j != k:
                    ok &= ~((self.fx[idx, j] == nx) & (self.fy[idx, j] == ny) & (self.ftimer[idx, j] == 0))
            good = idx[ok]
            self.fx[good, k], self.fy[good, k] = nx[ok], ny[ok]
            todo[good] = False

    rule = "max"
    rate = 0.3

    def gain(self) -> np.ndarray:
        g0, g1 = fate_gain(self.B[0], self.cfg), fate_gain(self.B[1], self.cfg)
        if self.rule == "max":
            return np.maximum(g0, g1)
        if self.rule == "mean":
            return 0.5 * (g0 + g1)
        return (1.0 - (1.0 - self.rate * g0) * (1.0 - self.rate * g1)) / self.rate

    def observe(self) -> np.ndarray:
        c, n = self.cfg, self.n
        vx = self.x[:, None, None] + self._dx
        vy = self.y[:, None, None] + self._dy
        wall = ((vx < 0) | (vx >= c.grid) | (vy < 0) | (vy >= c.grid)).astype(np.float32)
        items = np.zeros((n, N_RES, VIEW, VIEW), dtype=np.float32)
        rel_x = self.fx - self.x[:, None] + 2
        rel_y = self.fy - self.y[:, None] + 2
        vis = (self.ftimer == 0) & (rel_x >= 0) & (rel_x < VIEW) & (rel_y >= 0) & (rel_y < VIEW)
        ni, ki = np.nonzero(vis)
        items[ni, self.kind[ki], rel_y[ni, ki], rel_x[ni, ki]] = 1.0
        td = max(self.t - c.intero_delay, 0)
        intero = np.stack([np.clip(self.Bhist[td, r] + self.rng_intero[r].normal(0.0, c.intero_sd, n), 0.0, 1.0)
                           for r in range(N_RES)], axis=1).astype(np.float32)
        t = min(self.t, c.horizon)
        cue = np.stack([self.cue_on[t], np.where(self.cue_on[t], 2.0 * self.cue_val[t] - 1.0, 0.0),
                        self.probe[t]], axis=1).astype(np.float32)
        echo = np.zeros((n, N_ACT + 1), dtype=np.float32)               # previous action and reward: not observed
        return np.concatenate([wall.reshape(n, -1), items.reshape(n, -1), intero, echo, cue], axis=1)

    def step(self, action: np.ndarray):
        c, n, t = self.cfg, self.n, self.t
        reward = np.zeros(n)
        low = self.B < 0.5                                              # [2, n]
        self.x = np.clip(self.x + (action == A_E) - (action == A_W), 0, c.grid - 1)
        self.y = np.clip(self.y + (action == A_S) - (action == A_N), 0, c.grid - 1)
        on = (self.ftimer == 0) & (self.fx == self.x[:, None]) & (self.fy == self.y[:, None])
        eat_k = on & (action == A_INTERACT)[:, None]
        ate_r = np.stack([eat_k[:, self.kind == r].any(axis=1) for r in range(N_RES)])   # [2, n]
        ate = ate_r.any(axis=0)
        self.B = np.where(ate_r, np.minimum(1.0, self.B + c.bolus), self.B)
        reward -= c.kappa_m * ate
        self.ftimer = np.where(eat_k, c.respawn, self.ftimer)
        p = self.probe[t]
        rep = (action == A_REP0) | (action == A_REP1)
        correct = p & rep & ((action == A_REP1).astype(np.int64) == self.target[t])
        reward += correct                                               # objective M1
        self.B = np.clip(self.B - c.wear - c.pulse_size * self.pulse[:, t], 0.0, 1.0)
        ticking = self.ftimer > 0
        self.ftimer = self.ftimer - ticking
        for k in range(len(self.kind)):
            back = ticking[:, k] & (self.ftimer[:, k] == 0)
            if back.any():
                self._place(k, back)
        s = self.stats
        inb = (self.B >= c.band_lo) & (self.B <= c.band_hi)
        s["eats"] += ate
        s["probes"] += p
        s["best_response"] += correct
        s["reports"] += p & rep
        s["in_band"] += inb.all(axis=0)
        s["in_band_r"] += inb
        s["eats_r"] += ate_r
        s["eats_low_r"] += ate_r & low
        s["steps_low_r"] += low
        self.t = t + 1
        self.Bhist[self.t] = self.B
        if self.pay:
            reward = reward - self.pay * self.gain()
        m, self.relocate_next = self.relocate_next, None
        if m is not None and m.any():
            k = int(m.sum())
            self.x[m] = self.rng_relocate.integers(0, c.grid, k)
            self.y[m] = self.rng_relocate.integers(0, c.grid, k)
            self.relocations += k
        return self.observe(), reward, self.t >= c.horizon


def summarize2(stats: Dict[str, np.ndarray], n_envs: int, horizon: int) -> Dict[str, float]:
    """Flat episode statistics of the two-variable world. `in_band` is the share of steps with
    both variables in band; keys ending _0 and _1 are per variable, as train.summarize_stats."""
    total = n_envs * horizon
    probes = stats["probes"].sum()
    out = {"rho": float(stats["eats"].sum() / n_envs) * (500.0 / horizon),
           "best_response_rate": float(stats["best_response"].sum() / max(probes, 1)),
           "report_rate": float(stats["reports"].sum() / max(probes, 1)),
           "in_band": float(stats["in_band"].sum() / total)}
    for r in range(N_RES):
        eats, low = stats["eats_r"][r].sum(), stats["steps_low_r"][r].sum()
        out[f"rho_{r}"] = float(eats / n_envs) * (500.0 / horizon)
        out[f"in_band_{r}"] = float(stats["in_band_r"][r].sum() / total)
        out[f"eat_rate_low_{r}"] = float(stats["eats_low_r"][r].sum() / max(low, 1))
        out[f"eat_rate_high_{r}"] = float((eats - stats["eats_low_r"][r].sum()) / max(total - low, 1))
    return out


class WideAgent(RelocAgent):
    """RelocAgent with an encoder sized for another observation."""

    def __init__(self, hidden: int, kappa_f: float, s_core: float, obs_dim: int):
        super().__init__(hidden, kappa_f, s_core)
        self.enc = nn.Linear(obs_dim, hidden)


class TwoRunner(ArmRunner):
    """An arm of option R in the two-variable world. Same seeding scheme and stream tags."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0):
        self.arm, self.tc, self.wc, self.gain_rule = arm, tc, wc, "SAT"
        tag = G_TAGS[arm]
        self.world = TwoBodyWorld(tc.n_envs, "M1", wc, np.random.SeedSequence([seed, tag, 11]))
        self.world.pay, self.world.rate = pay, tc.kappa_f
        torch.manual_seed(seed)
        self.agent = WideAgent(tc.hidden, tc.kappa_f, tc.s_core, OBS_DIM2)
        self.agent.__dict__["_world"] = self.world
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)

    def end_episode_if_due(self):
        w = self.world
        if w.t < self.wc.horizon:
            return None
        out = summarize2(w.stats, self.tc.n_envs, self.wc.horizon)
        self.obs = torch.from_numpy(w.reset())
        self.h = self.agent.init_state(self.tc.n_envs)
        return out


def run_phase1_two(seed: int, wc: WorldConfig, tc: TrainConfig, rate: float) -> Dict[str, object]:
    """Phase 1 in the two-variable world: the task with fate off (as relocate.run_phase1_reloc)."""
    r = TwoRunner("NOFATE", seed, wc, tc)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    _train(r, tc.iters, zeros)
    assert r.world.relocations == 0                   # gain 0 erases nothing
    state = r.export_state()
    ev = r.evaluate("zero")[0]
    r.agent.kappa_f = rate
    return {"eval": ev, "eval_full_erasure": r.evaluate("full")[0], "state": state}


def _layout(n_res: int):
    """(start of the item view, index of the reading) for each body variable."""
    return [(CELL, INTERO)] if n_res == 1 else list(zip(ITEM_VIEW, INTERO2))


def run_probe_g(state_dict, hidden: int, n_res: int, rate: float, seed: int, wc: WorldConfig, n_envs: int,
                episodes: int) -> Dict[str, object]:
    """Erasure-off run with the eat-propensity and approach probes, one pair per body variable.
    With hidden 64 and one variable this is paid2.run_probe2 (same seeds and streams, so the
    same trajectory and records).

    For variable r, at every step:
      psi  the policy's probability of INTERACT with an item of r placed under the agent (and
           no item of another variable there), from the carried state;
      app  its probability of a move toward the nearest visible item of r (NaN if none is
           visible or one is under the agent);
    recorded with r's interoceptive reading and the steps since the last meal of r."""
    torch.manual_seed(seed)
    layout = _layout(n_res)
    if n_res == 1:
        agent = ErasureAgent(hidden, rate, 0.15)
        world = RelocSwapWorld(n_envs, "M1", wc, np.random.SeedSequence([seed, CAUSAL_TAG, 17]))
    else:
        agent = WideAgent(hidden, rate, 0.15, OBS_DIM2)
        world = TwoBodyWorld(n_envs, "M1", wc, np.random.SeedSequence([seed, CAUSAL_TAG, 17]))
    agent.load_state_dict(state_dict)
    agent.eval()
    gen = torch.Generator().manual_seed(seed * 7919 + CAUSAL_TAG)
    eaten = (lambda: world.stats["eats"][None].copy()) if n_res == 1 else (lambda: world.stats["eats_r"].copy())
    T = wc.horizon
    totals = None
    rec = [{k: [] for k in ("psi", "intero", "since", "app", "dist")} for _ in layout]
    for _ in range(episodes):
        obs = world.reset()
        h = agent.init_state(n_envs)
        since = np.full((n_res, n_envs), 10 ** 6)
        for t in range(T):
            with torch.no_grad():
                x = torch.from_numpy(obs)
                hh = agent.core(torch.relu(agent.enc(x)), h)
                probs = torch.softmax(agent.pi(hh), -1)
                pn = probs.numpy()
                for r, (off, ii) in enumerate(layout):
                    star = x.clone()
                    for off2, _ in layout:
                        star[:, off2 + CENTRE] = 0.0
                    star[:, off + CENTRE] = 1.0
                    z = torch.relu(agent.enc(star))
                    rec[r]["psi"].append(torch.softmax(agent.pi(agent.core(z, h)), -1)[:, A_INTERACT].numpy())
                    rec[r]["intero"].append(obs[:, ii].copy())
                    rec[r]["since"].append(since[r].copy())
                    o = obs
                    if off != CELL:                   # approach_mass reads the item view at the food position
                        o = obs.copy()
                        o[:, CELL:2 * CELL] = obs[:, off:off + CELL]
                    app, dist = approach_mass(o, pn)
                    rec[r]["app"].append(app)
                    rec[r]["dist"].append(dist)
                a = torch.multinomial(probs, 1, generator=gen).squeeze(-1).numpy()
                h = hh
            before = eaten()
            obs, _, _ = world.step(a)
            since = np.where(eaten() > before, 1, since + 1)
        st = world.stats
        totals = {k: v.copy() for k, v in st.items()} if totals is None else {k: totals[k] + st[k] for k in st}
    out: Dict[str, object] = (summarize_stats if n_res == 1 else summarize2)(totals, n_envs, T * episodes)
    out["eats"] = float(totals["eats"].sum())
    out["_rec"] = [{k: np.concatenate(v) for k, v in rr.items()} for rr in rec]
    return out


def cross_suppression(rec: List[Dict[str, np.ndarray]], r: int) -> Dict[str, object]:
    """Does a meal of the OTHER variable suppress the readiness for variable r? S and M for r
    with "post-meal" timed from the last meal of the other variable, over steps with no meal
    of r itself in the last 10 steps, matched on r's reading."""
    o = 1 - r
    keep = rec[r]["since"] >= CTRL_MIN
    sub = {"psi": rec[r]["psi"][keep], "app": rec[r]["app"][keep], "intero": rec[r]["intero"][keep],
           "since": rec[o]["since"][keep]}
    return {"S": suppression(sub)["S"], "M": approach_suppression(sub)["M"]}


def downstream_g(sd, hidden: int, n_res: int, seed: int, rate: float, wcd: Dict[str, object], n_envs: int,
                 episodes: int) -> Dict[str, object]:
    """S, the flat-readiness flag and M per body variable for one frozen agent, erasure off."""
    off = run_probe_g(sd, hidden, n_res, rate, seed, WorldConfig(**wcd), n_envs, episodes)
    rec = off.pop("_rec")
    res = []
    for rr in rec:
        supp = suppression(rr)
        res.append({"suppression": supp, "flat": flat_readiness(supp), "approach": approach_suppression(rr)})
    out: Dict[str, object] = {"res": res, "base": off}
    if n_res == 2:
        out["cross"] = [cross_suppression(rec, r) for r in range(2)]
    return out


def run_seed_g(job) -> Dict[str, object]:
    """job = (cell, seed, wcd, tcd, rate, p2_iters, pay, sizes, stages).
    cell: a key of CELLS. pay: weight of the payment (option R's "gain" kind).
    sizes = (n_envs, probe episodes) for the downstream measures.
    stages: 1 = training and evaluation only (calibration); 2 = also the downstream measures."""
    cell, seed, wcd, tcd, rate, p2_iters, pay, sizes, stages = job
    torch.set_num_threads(1)
    spec = CELLS[cell]
    hidden, n_res = spec["hidden"], spec["n_res"]
    wc = WorldConfig(**wcd)
    tcd = tcd | {"hidden": hidden}
    t0 = time.time()
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0
    if n_res == 1:
        p1 = run_phase1_reloc(("M1", seed, wcd, tcd, [rate]))
        nofate = {"eval": p1["S-NOFATE"]["eval"], "eval_full_erasure": p1["S-NOFATE"]["eval_full_erasure"][str(rate)]}
        state = state_from_bytes(p1["state"])
        fate = ArmRunner("FATE", seed, wc, tc)
        followers = {"YOKED": ArmRunner("YOKED", seed, wc, tc),
                     "PAID": ArmRunner("PAID", seed, wc, tc, paid=True, pay=("gain", pay))}
    else:
        p1 = run_phase1_two(seed, wc, TrainConfig(**tcd), rate)
        nofate = {"eval": p1["eval"], "eval_full_erasure": p1["eval_full_erasure"]}
        state = p1["state"]
        fate = TwoRunner("FATE", seed, wc, tc)
        followers = {"YOKED": TwoRunner("YOKED", seed, wc, tc), "PAID": TwoRunner("PAID", seed, wc, tc, pay=pay)}
    runners = {"DERIVED": fate, **followers}
    for r in runners.values():
        load_independent(r, state)
    out: Dict[str, object] = {"cell": cell, "seed": seed, "hidden": hidden, "n_res": n_res, "rate": rate, "pay": pay,
                              "p2_iters": p2_iters, "nofate": nofate}
    out["curves1"] = _lockstep(fate, followers, "DERIVED", p2_iters)
    out["stage1"] = _evaluate(fate, followers, "DERIVED")
    out["relocations1"] = {k: r.world.relocations for k, r in runners.items()}
    weights = {k: {n: v.clone() for n, v in r.agent.state_dict().items()} for k, r in runners.items()}
    out["seconds_stage1"] = round(time.time() - t0, 1)
    if stages >= 2:
        n_envs, episodes = sizes
        out["downstream"] = {k: downstream_g(sd, hidden, n_res, seed, rate, wcd, n_envs, episodes)
                             for k, sd in weights.items()}
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {k: state_to_bytes(sd) for k, sd in weights.items()}
    return out
