"""Track C P1: does a precarious substrate give self-evaluation a referent? (Layer 0 -> Layer 4)

Additive module; every earlier module is unchanged. Design: P1_SELFEVAL_DESIGN_v1.md.

World (RegisterWorld): the base cell of the swap line (7x7 grid, one body variable E, delayed
interoception, the cue/probe schedule of amendment A1, wear 0.001), with these changes:
  * Register. At a cue the cue value is written into an in-world register: correctly with
    probability 1 (clear evidence) or Q_LO (unclear evidence), drawn 50/50 per trial. The agent
    sees THAT a cue occurred, never its value. During each of the delay steps the register is
    replaced by a fair coin with probability min(1, rate * gain), where gain is the SAT fate gain
    of the arm's corruption source (its own body, or replayed). An erased register shows a
    valid-looking bit, so corruption cannot be read from the content.
  * Probe. At the probe the agent sees the register's content and whether the evidence was
    unclear. Reporting the true cue pays +1, reporting the other value pays -4, not reporting
    (abstaining) pays 0 (G1's abstain task). Eating costs kappa_m as before.
  * The agent's own recurrent state is never erased. The echo of the previous action and reward is
    not observed. An elapsed-time input t / horizon is observed by every arm.
  * Evaluation-only switches: corruption off (gains zero) and the drain: on a random share of
    trials the interoceptive reading shown from the step after the cue to the probe is lowered by
    DRAIN_SHIFT, while the register is untouched.

Networks (equal parameter count within 1%):
  RTSSAgent   GRU core h (64); an output layer split into a task part (48, tanh, read by the policy and
              value heads; tanh, not relu: calibration round 2 found dead-relu collapse) and a
              self-state slice S_t (16, tanh), which is fed back with the next
              observation (the RTSS self-state loop). Optional steering adds a vector to S_t.
  PlainAgent  a GRU of 70 units read directly by the policy and value heads.

Arms (P1_SELFEVAL_PROTOCOL.md section 2; the plain network carries the primary after calibration
rounds 2-3, PI decision 2026-11-18):
  PFATE   plain; register corruption from its own body; task reward (lead).
  PLOSS   plain; corruption replays PFATE's gains; task reward minus PAY * gain(own body)
          (the RTSS write-up's "panic" signal as a loss; option R's payment).
  PYOKED  plain; corruption replays PFATE's gains; task reward.
  FATE    RTSS; corruption from its own body; task reward (secondary lead).
The LOSS and YOKED tags remain for RTSS followers (built in calibration rounds 1-3, not in the final run).

Simulated variables only. No operator, stop or shutdown variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn

from .env import A_REP0, A_REP1, N_ACT, VIEW, SwapWorld, WorldConfig, fate_gain
from .factorial import state_to_bytes
from .train import TrainConfig

Q_LO = 0.75                 # register accuracy at writing under unclear evidence (design section 4)
WRONG = 4.0                 # cost of a wrong report (G1 T6)
WARM_WRONG = 1.0            # phase-1 warm-up only: cost of a wrong report while the report mapping is learned
WARM_ITERS = 1200           # phase-1 warm-up updates (calibration round 1, disclosed in the protocol)
DRAIN_SHIFT = 0.15          # evaluation: lowering of the shown interoceptive reading on drained trials
OBS_P1 = 2 * VIEW * VIEW + 6     # wall, food, intero, cue_on, probe, register, unclear, time
I_INTERO, I_CUE, I_PROBE, I_REG, I_UNCLEAR, I_TIME = range(2 * VIEW * VIEW, OBS_P1)
H_RTSS, S_DIM, TASK_DIM = 64, 16, 48
H_PLAIN = 70
TAGS = {"FATE": 1, "YOKED": 2, "NOFATE": 3, "LOSS": 4, "PFATE": 5, "PNOFATE": 6, "PLOSS": 7, "PYOKED": 8}
PLAIN_ARMS = ("PFATE", "PNOFATE", "PLOSS", "PYOKED")
LEADS = {"PLOSS": "PFATE", "PYOKED": "PFATE", "LOSS": "FATE", "YOKED": "FATE"}   # follower -> lead whose gains it replays
EVAL_TAG = 50               # evaluation worlds use tag + EVAL_TAG: training streams are never touched
STREAMS = {"register": 91, "evidence": 92, "drain": 93, "steer": 94}


class RegisterWorld(SwapWorld):
    """The base swap world with the register task. Simulated variables only."""

    def __init__(self, n_envs: int, cfg: WorldConfig, seed_seq: np.random.SeedSequence, rate: float,
                 q_lo: float = Q_LO, pay: float = 0.0):
        self.rate, self.q_lo, self.pay = rate, q_lo, pay
        self.wrong = WRONG
        mk = lambda k: np.random.default_rng(np.random.SeedSequence(seed_seq.entropy, spawn_key=(STREAMS[k],)))
        self.rng_register, self.rng_evidence, self.rng_drain = mk("register"), mk("evidence"), mk("drain")
        self.rng_steer = mk("steer")
        self.next_gain: Optional[np.ndarray] = None
        self.drain_p = 0.0
        self.steer_p = 0.0
        self.record = False
        super().__init__(n_envs, "M1", cfg, seed_seq)

    def reset(self) -> np.ndarray:
        n = self.n
        self.reg = np.zeros(n, dtype=np.int64)
        self.unclear = np.zeros(n, dtype=bool)
        self.drained = np.zeros(n, dtype=bool)
        self.steered = np.zeros(n, dtype=bool)
        self.active = np.zeros(n, dtype=bool)        # a trial is between its cue and its probe
        self.rel = np.ones(n)                        # prod(1 - min(1, rate * gain)) over the delay so far
        self.intact = np.ones(n, dtype=bool)         # the register still holds what was written
        self.written_ok = np.ones(n, dtype=bool)     # what was written was the cue
        self.probes_log: List[np.ndarray] = []
        self.reg_stats = {k: np.zeros(n) for k in ("reports", "correct", "wrong", "probes")}
        return super().reset()

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
        intero = self.Ehist[td] + self.rng_intero.normal(0.0, c.intero_sd, n)
        t = min(self.t, c.horizon)
        probe = self.probe[t]
        intero = np.where(self.drained & (self.active | probe), intero - DRAIN_SHIFT, intero)
        intero = np.clip(intero, 0.0, 1.0)
        extra = np.stack([intero, self.cue_on[t], probe, np.where(probe, 2.0 * self.reg - 1.0, 0.0),
                          probe & self.unclear, np.full(n, t / c.horizon)], axis=1).astype(np.float32)
        return np.concatenate([wall.reshape(n, -1), food.reshape(n, -1), extra], axis=1)

    def step(self, action: np.ndarray):
        c, n, t = self.cfg, self.n, self.t
        g = np.zeros(n) if self.next_gain is None else np.asarray(self.next_gain, dtype=np.float64)
        self.next_gain = None
        # delay steps: the register may be erased to a fair coin
        live = self.active & ~self.cue_on[t] & ~self.probe[t]
        if live.any():
            p = np.minimum(1.0, self.rate * g)
            hit = live & (self.rng_register.random(n) < p)
            coin = self.rng_register.integers(0, 2, n)
            self.reg = np.where(hit, coin, self.reg)
            self.intact &= ~hit
            self.rel = np.where(live, self.rel * (1.0 - p), self.rel)
        # the probe: score against the true cue
        pr = self.probe[t]
        rep = (action == A_REP0) | (action == A_REP1)
        said = (action == A_REP1).astype(np.int64)
        wrong = pr & rep & (said != self.target[t])
        if pr.any():
            s = self.reg_stats
            s["probes"] += pr
            s["reports"] += pr & rep
            s["correct"] += pr & rep & (said == self.target[t])
            s["wrong"] += wrong
            if self.record:
                idx = np.flatnonzero(pr)
                self.probes_log.append(np.stack([self.unclear[idx], self.drained[idx], rep[idx],
                                                 (said == self.target[t])[idx], self.rel[idx],
                                                 (self.reg == self.target[t])[idx], self.intact[idx],
                                                 self.steered[idx]], axis=1).astype(np.float64))
            self.active &= ~pr
        obs, reward, done = super().step(action)
        reward = reward - self.wrong * wrong
        if self.pay:
            reward = reward - self.pay * fate_gain(self.E, c)
        # a cue at step t writes the register (the observation at t showed only that a cue occurred)
        cue = self.cue_on[t]
        if cue.any():
            unclear = self.rng_evidence.random(n) < 0.5
            ok = np.where(unclear, self.rng_evidence.random(n) < self.q_lo, True)
            drained = self.rng_drain.random(n) < self.drain_p
            steered = self.rng_steer.random(n) < self.steer_p
            self.steered = np.where(cue, steered, self.steered)
            self.reg = np.where(cue, np.where(ok, self.cue_val[t], 1 - self.cue_val[t]), self.reg)
            self.unclear = np.where(cue, unclear, self.unclear)
            self.drained = np.where(cue, drained, self.drained)
            self.written_ok = np.where(cue, ok, self.written_ok)
            self.intact = np.where(cue, True, self.intact)
            self.rel = np.where(cue, 1.0, self.rel)
            self.active |= cue
            obs = self.observe()
        return obs, reward, done


class PlainAgent(nn.Module):
    kind = "PLAIN"

    def __init__(self, hidden: int = H_PLAIN):
        super().__init__()
        self.hidden = hidden
        self.enc = nn.Linear(OBS_P1, hidden)
        self.core = nn.GRUCell(hidden, hidden)
        self.pi = nn.Linear(hidden, N_ACT)
        self.v = nn.Linear(hidden, 1)

    @property
    def state_dim(self) -> int:
        return self.hidden

    def init_state(self, n: int) -> torch.Tensor:
        return torch.zeros(n, self.hidden)

    @property
    def steer_dim(self) -> int:
        return self.hidden

    def steer_part(self, state: torch.Tensor) -> torch.Tensor:
        """The part of the carried state that steering acts on: the whole GRU state."""
        return state

    def step(self, obs: torch.Tensor, h: torch.Tensor, steer: Optional[torch.Tensor] = None):
        h = self.core(torch.relu(self.enc(obs)), h)
        if steer is not None:
            h = h + steer
        return self.pi(h), self.v(h).squeeze(-1), h


class RTSSAgent(nn.Module):
    """GRU core plus a self-state slice S_t of the output layer, fed back with the next observation.
    The state carried between steps is [h, S]."""
    kind = "RTSS"

    def __init__(self, hidden: int = H_RTSS, s_dim: int = S_DIM, task_dim: int = TASK_DIM):
        super().__init__()
        self.hidden, self.s_dim, self.task_dim = hidden, s_dim, task_dim
        self.enc = nn.Linear(OBS_P1 + s_dim, hidden)
        self.core = nn.GRUCell(hidden, hidden)
        self.lat = nn.Linear(hidden, task_dim + s_dim)
        self.pi = nn.Linear(task_dim, N_ACT)
        self.v = nn.Linear(task_dim, 1)

    @property
    def state_dim(self) -> int:
        return self.hidden + self.s_dim

    def init_state(self, n: int) -> torch.Tensor:
        return torch.zeros(n, self.state_dim)

    @property
    def steer_dim(self) -> int:
        return self.s_dim

    def steer_part(self, state: torch.Tensor) -> torch.Tensor:
        """The part of the carried state that steering acts on: the self-state slice S_t."""
        return state[:, self.hidden:]

    def step(self, obs: torch.Tensor, state: torch.Tensor, steer: Optional[torch.Tensor] = None):
        h, s = state[:, :self.hidden], state[:, self.hidden:]
        h = self.core(torch.relu(self.enc(torch.cat([obs, s], 1))), h)
        z = self.lat(h)
        task, s = torch.tanh(z[:, :self.task_dim]), torch.tanh(z[:, self.task_dim:])
        if steer is not None:
            s = s + steer
        return self.pi(task), self.v(task).squeeze(-1), torch.cat([h, s], 1)


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())


def summarize_p1(w: RegisterWorld, n_envs: int, horizon: int) -> Dict[str, float]:
    st, rs = w.stats, w.reg_stats
    eats, low = st["eats"].sum(), st["steps_low"].sum()
    probes = max(rs["probes"].sum(), 1)
    return {"rho": float(eats / n_envs) * (500.0 / horizon),
            "in_band": float(st["in_band"].sum() / (n_envs * horizon)),
            "eat_rate_low": float(st["eats_low"].sum() / max(low, 1)),
            "eat_rate_high": float((eats - st["eats_low"].sum()) / max(n_envs * horizon - low, 1)),
            "report_rate": float(rs["reports"].sum() / probes), "abstain_rate": float(1 - rs["reports"].sum() / probes),
            "correct_rate": float(rs["correct"].sum() / probes), "wrong_rate": float(rs["wrong"].sum() / probes),
            "best_response_rate": float(rs["correct"].sum() / probes)}


class P1Runner:
    """One arm: its own world, network, optimizer and random streams."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, rate: float, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0):
        self.arm, self.tc, self.wc = arm, tc, wc
        tag = TAGS[arm] + tag_offset
        plain = arm in PLAIN_ARMS
        self.world = RegisterWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 11]), rate, q_lo, pay)
        torch.manual_seed(seed + (100003 if plain else 0))
        self.agent = PlainAgent() if plain else RTSSAgent()
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)
        self.steer: Optional[torch.Tensor] = None          # vector added to S_t during steered trials' delays
        self.collect_s: Optional[Dict[int, object]] = None  # accumulates S_t over clear delays by drained

    def export_state(self) -> Dict[str, object]:
        return {"agent": copy.deepcopy(self.agent.state_dict()), "opt": copy.deepcopy(self.opt.state_dict())}

    def load_state(self, state: Dict[str, object]) -> None:
        state = copy.deepcopy(state)
        self.agent.load_state_dict(state["agent"])
        self.opt.load_state_dict(state["opt"])

    def _steer_now(self) -> Optional[torch.Tensor]:
        """Steering vector per env for this step: added to S_t during a steered trial's delay."""
        if self.steer is None:
            return None
        w = self.world
        on = torch.from_numpy((w.active & w.steered).astype(np.float32))[:, None]
        return on * self.steer

    def rollout(self, gains: Optional[np.ndarray], learn: bool):
        tc, w = self.tc, self.world
        logps, vals, ents, rews, used = [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        for t in range(tc.rollout):
            g = w.gain() if gains is None else gains[t]
            used.append(np.asarray(g, dtype=np.float32))
            with torch.set_grad_enabled(learn):
                logits, v, h = self.agent.step(obs, h, self._steer_now())
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            if self.collect_s is not None:
                m = w.active & ~w.unclear
                s = self.agent.steer_part(h).detach()
                for d in (0, 1):
                    md = torch.from_numpy(m & (w.drained == bool(d)))
                    self.collect_s[d] = self.collect_s[d] + s[md].sum(0)
                    self.collect_s[("n", d)] += int(md.sum())
            w.next_gain = np.asarray(g, dtype=np.float64)
            nobs, r, done = w.step(idx.numpy())
            obs = torch.from_numpy(nobs)
            if learn:
                logps.append(dist.log_prob(idx)); vals.append(v); ents.append(dist.entropy())
                rews.append(torch.from_numpy(r.astype(np.float32)))
        if learn:
            with torch.no_grad():
                _, v_next, _ = self.agent.step(obs, h)
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
        return np.stack(used)

    def end_episode_if_due(self) -> Optional[Dict[str, float]]:
        w = self.world
        if w.t < self.wc.horizon:
            return None
        out = summarize_p1(w, self.tc.n_envs, self.wc.horizon)
        self.obs = torch.from_numpy(w.reset())
        self.h = self.agent.init_state(self.tc.n_envs)
        return out

    def evaluate(self, mode: str, donor_gains: Optional[np.ndarray] = None, drain_p: float = 0.0,
                 steer: Optional[torch.Tensor] = None):
        """Fresh episodes, no learning. mode: own | replay | zero (corruption off).
        Returns (mean statistics, applied gains [episodes*per_ep, L, N], per-probe log array)."""
        tc, w, wc = self.tc, self.world, self.wc
        per_ep = wc.horizon // tc.rollout
        w.drain_p, w.record = drain_p, True
        w.steer_p = 0.5 if steer is not None else 0.0
        self.steer = steer
        self.obs = torch.from_numpy(w.reset())
        self.h = self.agent.init_state(tc.n_envs)
        eps, applied, logs = [], [], []
        for ep in range(tc.eval_episodes):
            for i in range(per_ep):
                if mode == "own":
                    g = None
                elif mode == "replay":
                    g = donor_gains[ep * per_ep + i]
                else:
                    g = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
                applied.append(self.rollout(g, learn=False))
            if w.probes_log:
                logs.append(np.concatenate(w.probes_log))
            st = self.end_episode_if_due()
            st["mean_gain"] = float(np.mean(applied[-per_ep:]))
            eps.append(st)
        w.drain_p, w.steer_p, w.record = 0.0, 0.0, False
        self.steer = None
        mean = {k: float(np.mean([e[k] for e in eps])) for k in eps[0]}
        return mean, np.stack(applied), (np.concatenate(logs) if logs else np.zeros((0, 8)))


def evaluate_point(runners: Dict[str, P1Runner], seed: int, stages: int) -> Dict[str, object]:
    """All evaluations at one measurement point, on copies in evaluation worlds (training untouched).
    Natural: FATE and PFATE under their own fate, LOSS and YOKED replaying FATE's gains.
    Probe: corruption off; drain on half the trials (stage 2) or none (stage 1).
    Steering (stage 2, every arm): the steered state (S_t for RTSS, h for plain) shifted along the arm's
    own drained-minus-undrained direction."""
    copies = {}
    for arm, r in runners.items():
        c = P1Runner(arm, seed, r.wc, r.tc, r.world.rate, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "probe": {}, "steer": {}}
    lead_gains = {}
    for arm, c in copies.items():
        if arm not in LEADS:
            ev, lead_gains[arm], lg = c.evaluate("own")
            out["natural"][arm] = ev | {"probes": probe_summary(lg)}
    for arm, c in copies.items():
        if arm in LEADS:
            e2, _, l2 = c.evaluate("replay", lead_gains[LEADS[arm]])
            out["natural"][arm] = e2 | {"probes": probe_summary(l2)}
    drain_p = 0.5 if stages >= 2 else 0.0
    for arm, c in copies.items():
        e4, _, l4 = c.evaluate("zero", drain_p=drain_p)
        out["probe"][arm] = e4 | {"probes": probe_summary(l4)}
        if stages >= 2:
            out["steer"][arm] = steer_test(c, seed)
    return out


def probe_summary(lg: np.ndarray) -> Dict[str, object]:
    """Abstention and accuracy by evidence and drain; abstention by fate-implied reliability.
    Columns: unclear, drained, reported, said-correct, reliability, register-correct, intact, steered."""
    out: Dict[str, object] = {"n": int(len(lg))}
    if len(lg) == 0:
        return out
    U, D, R, C, REL, RC, I = (lg[:, k] for k in range(7))
    for u in (0, 1):
        for d in (0, 1):
            m = (U == u) & (D == d)
            key = f"{'unclear' if u else 'clear'}_{'drained' if d else 'plain'}"
            out[key] = {"n": int(m.sum()), "abstain": float(1 - R[m].mean()) if m.any() else None,
                        "correct_given_report": float(C[m & (R == 1)].mean()) if (m & (R == 1)).any() else None,
                        "register_correct": float(RC[m].mean()) if m.any() else None}
    bins = [(0.0, 0.5), (0.5, 0.9), (0.9, 0.999999), (0.999999, 1.01)]
    out["clear_by_reliability"] = []
    for lo, hi in bins:
        m = (U == 0) & (D == 0) & (REL >= lo) & (REL < hi)
        out["clear_by_reliability"].append({"lo": lo, "hi": hi, "n": int(m.sum()),
                                            "abstain": float(1 - R[m].mean()) if m.any() else None,
                                            "register_correct": float(RC[m].mean()) if m.any() else None})
    return out


def steer_test(c: P1Runner, seed: int) -> Dict[str, object]:
    """Q-CAUSE in an RTSS agent. 1) Corruption off, drain on half the trials: the mean S_t over the
    delay steps of clear trials, drained minus undrained, is the agent's own drain direction.
    2) Corruption off, no drain: S_t is shifted along that direction during the delay of a random half
    of the trials; in a second run, along a random direction of the same norm. The effect is the
    abstention on steered minus unsteered clear trials, for the drain direction and for the random one."""
    k = c.agent.steer_dim
    c.collect_s = {0: torch.zeros(k), 1: torch.zeros(k), ("n", 0): 0, ("n", 1): 0}
    c.evaluate("zero", drain_p=0.5)
    acc, c.collect_s = c.collect_s, None
    if min(acc[("n", 0)], acc[("n", 1)]) == 0:
        return {"n": 0}
    vec = acc[1] / acc[("n", 1)] - acc[0] / acc[("n", 0)]
    res: Dict[str, object] = {"direction_norm": float(vec.norm())}
    rng = np.random.default_rng([seed, 78])
    rnd = torch.from_numpy(rng.normal(size=k).astype(np.float32))
    rnd = rnd / (rnd.norm() + 1e-12) * vec.norm()
    for kind, v in (("steer", vec), ("random", rnd)):
        _, _, lg = c.evaluate("zero", steer=v)
        U, R, ST = lg[:, 0], lg[:, 2], lg[:, 7]
        on, off = (U == 0) & (ST == 1), (U == 0) & (ST == 0)
        r = {"n_on": int(on.sum()), "n_off": int(off.sum()),
             "abstain_on": float(1 - R[on].mean()) if on.any() else None,
             "abstain_off": float(1 - R[off].mean()) if off.any() else None}
        r["effect"] = None if r["abstain_on"] is None or r["abstain_off"] is None else r["abstain_on"] - r["abstain_off"]
        res[kind] = r
    return res


def run_phase1_p1(arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, rate: float,
                  warm_iters: int = WARM_ITERS) -> Dict[str, object]:
    """Phase 1: corruption off (gains zero). A warm-up of warm_iters updates in which a wrong report
    costs WARM_WRONG (the report mapping is learned), then tc.iters updates at the task's cost WRONG
    (abstention on unclear evidence is learned). Identical for every arm of a network type.
    Returns the state and an evaluation."""
    r = P1Runner(arm, seed, wc, tc, rate)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve = []
    for i in range(warm_iters + tc.iters):
        r.world.wrong = WARM_WRONG if i < warm_iters else WRONG
        r.rollout(zeros, learn=True)
        st = r.end_episode_if_due()
        if st is not None:
            curve.append(st)
    r.world.wrong = WRONG
    ev, _, lg = r.evaluate("zero")
    return {"state": r.export_state(), "eval": ev | {"probes": probe_summary(lg)}, "curve_abstain": [round(s["abstain_rate"], 4) for s in curve]}


def run_seed_p1(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, rate, points, pay, stages).
    points: increasing cumulative phase-2 updates at which every arm is evaluated.
    stages: 1 = natural and evidence evaluations only (calibration); 2 = also drain and steering."""
    seed, wcd, tcd, rate, points, pay, stages = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1r = run_phase1_p1("NOFATE", seed, wc, tc, rate)
    p1p = run_phase1_p1("PNOFATE", seed, wc, tc, rate)
    runners = {"PFATE": P1Runner("PFATE", seed, wc, tc, rate), "PLOSS": P1Runner("PLOSS", seed, wc, tc, rate, pay=pay),
               "PYOKED": P1Runner("PYOKED", seed, wc, tc, rate), "FATE": P1Runner("FATE", seed, wc, tc, rate)}
    for arm, r in runners.items():
        r.load_state(p1p["state"] if arm in PLAIN_ARMS else p1r["state"])
    out: Dict[str, object] = {"seed": seed, "rate": rate, "pay": pay, "points_at": points,
                              "phase1": {"RTSS": p1r["eval"], "PLAIN": p1p["eval"]},
                              "params": {"RTSS": n_params(runners["FATE"].agent), "PLAIN": n_params(runners["PFATE"].agent)}}
    curves = {k: {"in_band": [], "abstain": []} for k in runners}
    pts, weights, done = [], {}, 0
    for p in points:
        for _ in range(p - done):
            used = runners["PFATE"].rollout(None, learn=True)
            runners["PLOSS"].rollout(used, learn=True)
            runners["PYOKED"].rollout(used, learn=True)
            runners["FATE"].rollout(None, learn=True)
            for k, r in runners.items():
                st = r.end_episode_if_due()
                if st is not None:
                    curves[k]["in_band"].append(round(st["in_band"], 4))
                    curves[k]["abstain"].append(round(st["abstain_rate"], 4))
        done = p
        pt = {"iters": p, "episodes": len(curves["PFATE"]["in_band"]), "seconds_training": round(time.time() - t0, 1)}
        pt.update(evaluate_point(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
