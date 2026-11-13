"""Track C swap, option R2: replication of derived against paid, with a relocation control.

Additive module; every earlier module is unchanged. Option R (TRACKC_PAID_RESULTS.md) found
derived regulators ahead of paid ones on the anticipation index, and, post hoc, that some
derived agents do not gate the eat action at all. R2 repeats stage 1 of R on fresh seeds and
adds two things.

1. A fourth arm, PAIDR. In this world an erasure also relocates the agent, so a derived
   agent's position is tied to its own E and a paid agent's is not. PAIDR separates the two
   parts of the dependence:
     memory erasure  replays the derived agent's gains (as PAID: independent of its own E);
     relocation      follows its own E (probability rate * g(E) per step, as DERIVED);
     reward          task plus the same homeostatic payment as PAID.
   A replayed erasure does not relocate PAIDR, and its own relocation does not erase.

2. An approach probe, recorded beside option Q's eat-propensity probe in the same run.
   At every step where food is visible and not under the agent, the policy's probability of
   a move that brings it closer to the nearest visible food is read from the actual
   observation and the carried state (nothing is modified):
     psi_approach = sum of the policy's probability over such moves.
   Post-meal steps are compared with control steps at the same interoceptive reading, as
   for S. The index M is to moving toward food what S is to the eat action.

Arms DERIVED, YOKED and PAID are built exactly as in option R (same classes and seeding).
Every agent loads its own deep copy of the phase-1 state (TRACKC_SWAP_ERRATUM_1.md).

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from .causal import BINS, CAUSAL_TAG, CTRL_MIN, FOOD_HERE, INTERO, MIN_BIN, MIN_POST, POST, suppression
from .env import A_E, A_INTERACT, A_N, A_S, A_W, VIEW, WorldConfig
from .erasure import ErasureAgent
from .factorial import state_from_bytes, state_to_bytes
from .paid import ArmRunner, PaidRelocWorld, _evaluate, _lockstep, load_independent
from .probe import decode, run_agent
from .relocate import RelocAgent, RelocSwapWorld, run_phase1_reloc
from .train import TrainConfig, summarize_stats

PAIDR_TAG = 7                                  # world and generator streams of PAIDR (1, 2, 4-6 are option R's)
SPLIT_STREAM = 13                              # PAIDR's own relocation draws
FLAT_MIN = 0.40                                # flat eat readiness: psi_ctrl at least this in every upper bin
FLAT_BINS = (1, 2, 3)                          # readings 0.35-0.40, 0.40-0.45, 0.45-0.50
_OFF = np.arange(VIEW) - VIEW // 2
_DX = np.tile(_OFF, (VIEW, 1))[None]           # column offset of each view cell
_DY = np.tile(_OFF[:, None], (1, VIEW))[None]  # row offset
_DIST = np.abs(_DX) + np.abs(_DY)              # Manhattan distance from the agent
FAR = 99


class SplitAgent(RelocAgent):
    """Memory erasure follows the gain it is given (replayed). Relocation follows the gain of
    its own world, drawn from the world's own stream `rng_split`."""

    def step(self, obs: torch.Tensor, h: torch.Tensor, gain: torch.Tensor, gen: torch.Generator):
        h = self.core(torch.relu(self.enc(obs)), h)
        logits, value = self.pi(h), self.v(h).squeeze(-1)
        if gain is not None:
            p = torch.clamp(self.kappa_f * gain, 0.0, 1.0)
            erase = torch.rand(p.shape, generator=gen) < p
            h = h * (~erase).to(h.dtype)[:, None]
            world = self.__dict__.get("_world")
            if world is not None:
                own = np.clip(self.kappa_f * world.gain(), 0.0, 1.0)
                world.relocate_next = world.rng_split.random(own.shape) < own
        return logits, value, h


class SplitRunner(ArmRunner):
    """The PAIDR arm: paid world, SplitAgent."""

    def __init__(self, seed: int, wc: WorldConfig, tc: TrainConfig, pay=("gain", 1.0)):
        self.arm, self.tc, self.wc, self.gain_rule = "PAIDR", tc, wc, "SAT"
        tag = PAIDR_TAG
        self.world = PaidRelocWorld(tc.n_envs, "M1", wc, np.random.SeedSequence([seed, tag, 11]))
        self.world.pay_kind, self.world.pay = pay
        self.world.rng_split = np.random.default_rng(np.random.SeedSequence([seed, tag, SPLIT_STREAM]))
        torch.manual_seed(seed)
        self.agent = SplitAgent(tc.hidden, tc.kappa_f, tc.s_core)
        self.agent.__dict__["_world"] = self.world
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)


def approach_mass(obs: np.ndarray, probs: np.ndarray):
    """Policy probability of a move toward the nearest visible food, per environment.
    NaN where no food is visible or food is under the agent. Also returns the distance."""
    n = obs.shape[0]
    food = obs[:, VIEW * VIEW:2 * VIEW * VIEW].reshape(n, VIEW, VIEW) > 0.5
    here = food[:, VIEW // 2, VIEW // 2].copy()
    d = np.where(food, _DIST, FAR)
    d[:, VIEW // 2, VIEW // 2] = FAR
    dmin = d.reshape(n, -1).min(axis=1)
    near = (d == dmin[:, None, None]) & (dmin[:, None, None] < FAR)
    mass = (probs[:, A_E] * (near & (_DX > 0)).any(axis=(1, 2)) + probs[:, A_W] * (near & (_DX < 0)).any(axis=(1, 2))
            + probs[:, A_S] * (near & (_DY > 0)).any(axis=(1, 2)) + probs[:, A_N] * (near & (_DY < 0)).any(axis=(1, 2)))
    valid = (dmin < FAR) & ~here
    return np.where(valid, mass, np.nan), np.where(valid, dmin, FAR)


def run_probe2(state_dict, rate: float, seed: int, wc: WorldConfig, n_envs: int, episodes: int) -> Dict[str, object]:
    """Option Q's erasure-off run with its eat-propensity probe (same seeds and streams as
    causal.run_mode(..., "off", probe=True), so the trajectory is identical), also recording
    the approach probe."""
    torch.manual_seed(seed)
    agent = ErasureAgent(64, rate, 0.15)
    agent.load_state_dict(state_dict)
    agent.eval()
    world = RelocSwapWorld(n_envs, "M1", wc, np.random.SeedSequence([seed, CAUSAL_TAG, 17]))
    gen = torch.Generator().manual_seed(seed * 7919 + CAUSAL_TAG)
    T = wc.horizon
    totals = None
    rec = {k: [] for k in ("psi", "psi0", "intero", "E", "since", "app", "dist")}
    for _ in range(episodes):
        obs = world.reset()
        h = agent.init_state(n_envs)
        since = np.full(n_envs, 10 ** 6)
        for t in range(T):
            with torch.no_grad():
                x = torch.from_numpy(obs)
                star = x.clone()
                star[:, FOOD_HERE] = 1.0
                z = torch.relu(agent.enc(star))
                rec["psi"].append(torch.softmax(agent.pi(agent.core(z, h)), -1)[:, A_INTERACT].numpy())
                rec["psi0"].append(torch.softmax(agent.pi(agent.core(z, torch.zeros_like(h))), -1)[:, A_INTERACT].numpy())
                rec["intero"].append(obs[:, INTERO].copy())
                rec["E"].append(world.E.copy())
                rec["since"].append(since.copy())
                hh = agent.core(torch.relu(agent.enc(x)), h)
                probs = torch.softmax(agent.pi(hh), -1)
                app, dist = approach_mass(obs, probs.numpy())
                rec["app"].append(app)
                rec["dist"].append(dist)
                a = torch.multinomial(probs, 1, generator=gen).squeeze(-1).numpy()
                h = hh
            before = world.stats["eats"].copy()
            obs, _, _ = world.step(a)
            ate = world.stats["eats"] > before
            since = np.where(ate, 1, since + 1)
        st = world.stats
        totals = {k: v.copy() for k, v in st.items()} if totals is None else {k: totals[k] + st[k] for k in st}
    out: Dict[str, object] = summarize_stats(totals, n_envs, T * episodes)
    out["eats"] = float(totals["eats"].sum())
    out["_rec"] = {k: np.concatenate(v) for k, v in rec.items()}
    return out


def approach_suppression(rec) -> Dict[str, object]:
    """Post-meal suppression of the approach to food, matched on the interoceptive reading.
    As causal.suppression, with psi_approach in place of the eat propensity, over steps
    where it is defined:
      M = 1 - sum_b n_post_b * mean_post_b / sum_b n_post_b * mean_ctrl_b."""
    app, intero, since = rec["app"], rec["intero"], rec["since"]
    ok = ~np.isnan(app)
    post = ok & (since >= POST[0]) & (since <= POST[1])
    ctrl = ok & (since >= CTRL_MIN)
    num = den = 0.0
    n_used = 0
    per_bin = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        b = (intero >= lo) & (intero < hi)
        npost, nctrl = int((b & post).sum()), int((b & ctrl).sum())
        if npost >= MIN_BIN and nctrl >= MIN_BIN:
            mp, mc = float(app[b & post].mean()), float(app[b & ctrl].mean())
            num += npost * mp
            den += npost * mc
            n_used += npost
            per_bin.append({"lo": lo, "hi": hi, "n_post": npost, "n_ctrl": nctrl, "app_post": mp, "app_ctrl": mc,
                            "M": 1.0 - mp / mc if mc > 0 else None})
        else:
            per_bin.append({"lo": lo, "hi": hi, "n_post": npost, "n_ctrl": nctrl, "app_post": None,
                            "app_ctrl": None, "M": None})
    M = (1.0 - num / den) if (n_used >= MIN_POST and den > 0) else None
    return {"M": M, "n_post": n_used, "per_bin": per_bin}


def flat_readiness(supp: Dict[str, object]):
    """True if the eat propensity at control steps is at least FLAT_MIN in every populated
    bin of the reading from 0.35 to 0.50 (option R's post-hoc definition). None if fewer than
    two of those bins are populated."""
    vals = [supp["per_bin"][i]["psi_ctrl"] for i in FLAT_BINS]
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return None
    return bool(min(vals) >= FLAT_MIN)


def downstream2(sd, seed: int, rate: float, wcd: Dict[str, object], n_envs: int, probe_eps: int,
                causal_eps: int) -> Dict[str, object]:
    """Option P's decoding, the interoception shuffle, S, the flat-readiness flag and M for
    one frozen agent, erasure off."""
    wc = WorldConfig(**wcd)
    out: Dict[str, object] = {}
    intact = run_agent(sd, "M1", seed, wc, n_envs, probe_eps, False, True)
    out.update(decode(intact.pop("_rec")))
    out["intact"] = intact
    out["shuffled"] = run_agent(sd, "M1", seed, wc, n_envs, probe_eps, True, False)
    off = run_probe2(sd, rate, seed, wc, n_envs, causal_eps)
    rec = off.pop("_rec")
    out["suppression"] = suppression(rec)
    out["flat"] = flat_readiness(out["suppression"])
    out["approach"] = approach_suppression(rec)
    out["base"] = off
    return out


def run_seed2(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, rate, p2_iters, pay, sizes, stages).
    sizes = (n_envs, probe episodes, causal episodes) for the downstream measures.
    stages: 1 = training and evaluation only (calibration); 2 = also the downstream measures."""
    seed, wcd, tcd, rate, p2_iters, pay, sizes, stages = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    p1 = run_phase1_reloc(("M1", seed, wcd, tcd, [rate]))
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0
    state = state_from_bytes(p1["state"])
    fate = ArmRunner("FATE", seed, wc, tc)
    followers = {"YOKED": ArmRunner("YOKED", seed, wc, tc),
                 "PAID": ArmRunner("PAID", seed, wc, tc, paid=True, pay=pay),
                 "PAIDR": SplitRunner(seed, wc, tc, pay=pay)}
    for r in (fate, *followers.values()):
        load_independent(r, state)
    out: Dict[str, object] = {"seed": seed, "rate": rate, "pay": list(pay), "p2_iters": p2_iters,
                              "nofate": {"eval": p1["S-NOFATE"]["eval"],
                                         "eval_full_erasure": p1["S-NOFATE"]["eval_full_erasure"][str(rate)]}}
    out["curves1"] = _lockstep(fate, followers, "DERIVED", p2_iters)
    out["stage1"] = _evaluate(fate, followers, "DERIVED")
    out["relocations1"] = {"DERIVED": fate.world.relocations, **{k: r.world.relocations for k, r in followers.items()}}
    weights = {"DERIVED": fate.agent.state_dict(), **{k: r.agent.state_dict() for k, r in followers.items()}}
    weights = {k: {n: v.clone() for n, v in sd.items()} for k, sd in weights.items()}
    out["seconds_stage1"] = round(time.time() - t0, 1)
    if stages >= 2:
        n_envs, probe_eps, causal_eps = sizes
        out["downstream"] = {k: downstream2(sd, seed, rate, wcd, n_envs, probe_eps, causal_eps)
                             for k, sd in weights.items()}
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {k: state_to_bytes(sd) for k, sd in weights.items()}
    return out
