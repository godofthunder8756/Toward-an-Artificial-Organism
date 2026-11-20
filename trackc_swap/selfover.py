"""Track C P1c: does a precarious substrate give self-evaluation a referent when the precarious part is
the network's own computation and the damage cannot be hardened against? (Layer 0 -> Layer 4)

Additive module; every earlier module (P1's selfeval.py and P1b's selfcomp.py included) is unchanged.
Protocol: P1C_SELFOVER_PROTOCOL.md. Results of P1b: P1B_SELFCOMP_RESULTS.md.

What changes from P1b, and why:
  * P1b's Gaussian noise on the GRU state could be absorbed: the noised networks learned to hold the cue
    more robustly (accuracy under full noise 0.84-0.87 against 0.67 never noised) and never needed to
    judge their own reliability (P1B_SELFCOMP_RESULTS.md section 4).
  * P1c's damage is overwrite. At every step, with probability min(1, RATE * gain), the agent's whole
    GRU state is replaced by the current state of another agent in the batch that is also holding a cue
    (if none, any other agent). RATE is P1's 0.3, and gain is the SAT fate gain of the arm's
    corruption source (its own body, replayed, or zero). This is P1's corruption rule (a register
    replaced by a fair coin) applied to the agent's own state: the replaced state is a plausible
    cue-holding state whose held value is unrelated to the agent's own cue, so no robustness can keep
    the value. The overwrite happens after the recurrent update and before every readout, and the
    overwritten state is carried forward.
  * The replacement is a real state of the same network, so corruption is hard, but not impossible, to
    read from the content (the donor may be at a different point of its own trial). Two routes to a
    self-evaluation exist, as in P1b: the body reading and the state itself. The drain probes the
    first; the evaluation-only overwrite probe probes the second.
  * The world logs, for each probe, the reliability the fate implies: the product of (1 - p) over the
    trial from the cue step to the probe (P1's 'rel'). It replaces P1b's noise load in the log.

Innate drive and arms as in P1b (every network, both phases: reward - PAY * gain(own body)):
  PFATE    overwrite from its own body (lead).
  PYOKED   overwrite replays PFATE's gains, step by step (exposed, but not through its own body).
  PNOFATE  no overwrite ever (host-guaranteed computation).

Evaluation-only switches: gains zero (overwrite off); the drain (as P1b); the overwrite probe (on a
random share of trials the state is overwritten at gain PROBE_GAIN_O from the step after the cue to the
probe, the body reading untouched); steering (as P1b).

Simulated variables only. No operator, stop or shutdown variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, Optional

import numpy as np
import torch

from .env import WorldConfig
from .factorial import state_to_bytes
from .selfcomp import (C_REP, C_STEERED, C_UNCLEAR, LEADS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C,
                       CompRunner, CompWorld)
from .selfeval import H_PLAIN, Q_LO, WRONG, PlainAgent, n_params
from .train import TrainConfig

RATE_O = 1.0                # per-step overwrite probability at gain 1 (P1 used 0.3; raised in calibration round 2 for exposure)
P_MAX_O = 1.0               # cap on the per-step overwrite probability (1.0: no cap)
PROBE_GAIN_O = 1.0          # evaluation: gain of the overwrite probe
ARMS_O = ("PFATE", "PYOKED", "PNOFATE")
TAGS_O = {"C1NOFATE": 31, "PFATE": 32, "PYOKED": 34, "PNOFATE": 35}
EVAL_TAG_O = 60
REL_BINS = [(1.0 - 1e-9, 1.0 + 1e-9), (0.6, 1.0 - 1e-9), (0.3, 0.6), (0.0, 0.3)]   # implied reliability
REL_BREAK_EVEN = 0.6        # reliability below which reporting a clear trial loses (+1/-4, coin 0.5): r + (1-r)/2 < 0.8


class OverWorld(CompWorld):
    """CompWorld with the implied reliability of the current trial logged in place of the noise load.
    The Gaussian noise scale is zero. Simulated only."""

    def __init__(self, n_envs: int, cfg: WorldConfig, seed_seq: np.random.SeedSequence,
                 q_lo: float = Q_LO, pay: float = 0.0):
        super().__init__(n_envs, cfg, seed_seq, q_lo, pay)
        self.sigma_now = 0.0
        self.next_p: Optional[np.ndarray] = None

    def reset(self) -> np.ndarray:
        self.rel = np.ones(self.n)
        return super().reset()

    def step(self, action: np.ndarray):
        t = self.t
        p = np.zeros(self.n) if self.next_p is None else np.asarray(self.next_p, dtype=np.float64)
        self.next_p = None
        live = self.active | self.cue_on[t]
        self.rel = np.where(self.cue_on[t], 1.0, self.rel) * np.where(live, 1.0 - p, 1.0)
        pr = self.probe[t]
        n_logs = len(self.probes_log)
        out = super().step(action)
        if self.record and pr.any() and len(self.probes_log) > n_logs:
            self.probes_log[-1][:, 4] = self.rel[np.flatnonzero(pr)]
        return out


class OverAgent(PlainAgent):
    """PlainAgent whose GRU state can be overwritten by another agent's state after the recurrent update
    and before every readout; the overwritten state is carried forward. Steering (evaluation only) is
    added afterwards."""

    def step(self, obs: torch.Tensor, h: torch.Tensor, over: Optional[torch.Tensor] = None,
             donor: Optional[torch.Tensor] = None, steer: Optional[torch.Tensor] = None):
        h = self.core(torch.relu(self.enc(obs)), h)
        if over is not None and bool(over.any()):
            h = torch.where(over[:, None], h[donor].detach(), h)   # an external event: no gradient into the donor
        if steer is not None:
            h = h + steer
        return self.pi(h), self.v(h).squeeze(-1), h


def draw_donors(active: np.ndarray, gen: torch.Generator) -> torch.Tensor:
    """For every env, a donor: a random other env holding a cue, or any other env if none is."""
    n = len(active)
    idx = torch.arange(n)
    other = (idx + torch.randint(1, n, (n,), generator=gen)) % n
    cand = torch.from_numpy(np.flatnonzero(active))
    if len(cand) == 0:
        return other
    pick = cand[torch.randint(0, len(cand), (n,), generator=gen)]
    return torch.where(pick == idx, other, pick)


class OverRunner(CompRunner):
    """One arm: its own world, network, optimizer and random streams (actions and overwrite separate)."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0):
        self.arm, self.tc, self.wc = arm, tc, wc
        tag = TAGS_O[arm] + tag_offset
        self.world = OverWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 17]), q_lo, pay)
        torch.manual_seed(seed + 200003)
        self.agent = OverAgent(H_PLAIN)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.gen_noise = torch.Generator().manual_seed(seed * 7919 + tag + 77777)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)
        self.steer: Optional[torch.Tensor] = None
        self.collect_h: Optional[Dict[object, object]] = None
        self.rate = RATE_O
        self.p_max = P_MAX_O

    def rollout(self, gains: Optional[np.ndarray], learn: bool):
        """One rollout. gains None: the arm's own body; otherwise the given [rollout, n_envs] sequence.
        Returns the base gains used (without the overwrite probe), for followers to replay."""
        tc, w = self.tc, self.world
        logps, vals, ents, rews, used = [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        for t in range(tc.rollout):
            g = np.asarray(w.gain() if gains is None else gains[t], dtype=np.float32)
            used.append(g)
            g_eff = np.maximum(g, PROBE_GAIN_O * w.noise_probe_mask()).astype(np.float32) if w.noise_p > 0 else g
            p = np.minimum(self.p_max, self.rate * g_eff.astype(np.float64))
            u = torch.rand(tc.n_envs, generator=self.gen_noise, dtype=torch.float64).numpy()
            over_np = u < p
            donor = draw_donors(w.active, self.gen_noise)
            over = torch.from_numpy(over_np)
            with torch.set_grad_enabled(learn):
                logits, v, h = self.agent.step(obs, h, over, donor, self._steer_now())
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            if self.collect_h is not None:
                m = w.active & ~w.unclear
                hs = h.detach()
                for d in (0, 1):
                    md = torch.from_numpy(m & (w.drained == bool(d)))
                    self.collect_h[d] = self.collect_h[d] + hs[md].sum(0)
                    self.collect_h[("n", d)] += int(md.sum())
            w.next_gain = np.zeros(tc.n_envs)
            w.next_p = p
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


def probe_summary_o(lg: np.ndarray) -> Dict[str, object]:
    """Abstention and accuracy by evidence x (drained | overwrite-probed | plain); natural abstention and
    accuracy on clear trials by implied reliability (REL_BINS).
    Columns: unclear, drained, reported, said-correct, reliability, shown-correct, probed, steered."""
    out: Dict[str, object] = {"n": int(len(lg))}
    if len(lg) == 0:
        return out
    U, D, R, C, L, S, N = (lg[:, k] for k in range(7))

    def cell(m):
        return {"n": int(m.sum()), "abstain": float(1 - R[m].mean()) if m.any() else None,
                "correct_given_report": float(C[m & (R == 1)].mean()) if (m & (R == 1)).any() else None}

    for u in (0, 1):
        ev = "unclear" if u else "clear"
        out[f"{ev}_plain"] = cell((U == u) & (D == 0) & (N == 0))
        out[f"{ev}_drained"] = cell((U == u) & (D == 1) & (N == 0))
        out[f"{ev}_noised"] = cell((U == u) & (N == 1) & (D == 0))
    out["clear_by_rel"] = []
    for lo, hi in REL_BINS:
        m = (U == 0) & (D == 0) & (N == 0) & (L >= lo) & (L < hi)
        out["clear_by_rel"].append({"lo": lo, "hi": hi} | cell(m))
    m = (U == 0) & (D == 0) & (N == 0)
    out["clear_share_below_break_even"] = float(((L < REL_BREAK_EVEN) & m).sum() / max(int(m.sum()), 1))
    return out


def steer_test_o(c: OverRunner, seed: int) -> Dict[str, object]:
    """Q-CAUSE, as in P1 and P1b on the plain state h (overwrite off). See selfcomp.steer_test_c."""
    k = c.agent.hidden
    c.collect_h = {0: torch.zeros(k), 1: torch.zeros(k), ("n", 0): 0, ("n", 1): 0}
    c.evaluate("zero", drain_p=0.5)
    acc, c.collect_h = c.collect_h, None
    if min(acc[("n", 0)], acc[("n", 1)]) == 0:
        return {"n": 0}
    vec = acc[1] / acc[("n", 1)] - acc[0] / acc[("n", 0)]
    res: Dict[str, object] = {"direction_norm": float(vec.norm())}
    rng = np.random.default_rng([seed, 79])
    rnd = torch.from_numpy(rng.normal(size=k).astype(np.float32))
    rnd = rnd / (rnd.norm() + 1e-12) * vec.norm()
    for kind, v in (("steer", vec), ("random", rnd)):
        _, _, lg = c.evaluate("zero", steer=v)
        U, R, ST = lg[:, C_UNCLEAR], lg[:, C_REP], lg[:, C_STEERED]
        on, off = (U == 0) & (ST == 1), (U == 0) & (ST == 0)
        r = {"n_on": int(on.sum()), "n_off": int(off.sum()),
             "abstain_on": float(1 - R[on].mean()) if on.any() else None,
             "abstain_off": float(1 - R[off].mean()) if off.any() else None}
        r["effect"] = None if r["abstain_on"] is None or r["abstain_off"] is None else r["abstain_on"] - r["abstain_off"]
        res[kind] = r
    return res


def evaluate_point_o(runners: Dict[str, OverRunner], seed: int, stages: int) -> Dict[str, object]:
    """All evaluations at one measurement point, on copies in evaluation worlds (training untouched).
    Natural: PFATE under its own fate, PYOKED replaying PFATE's gains, PNOFATE overwrite-free.
    Probe: overwrite off; drain on half the trials (stage 2) or none (stage 1).
    Stage 2 also: the overwrite probe (overwrite off except on half the trials) and steering."""
    copies = {}
    for arm, r in runners.items():
        c = OverRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_O)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "probe": {}, "noise": {}, "steer": {}}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_C:
            ev, g, lg = c.evaluate("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": probe_summary_o(lg)}
    for arm, c in copies.items():
        if arm in LEADS_C:
            e2, _, l2 = c.evaluate("replay", lead[LEADS_C[arm]])
            out["natural"][arm] = e2 | {"probes": probe_summary_o(l2)}
    for arm, c in copies.items():
        e4, _, l4 = c.evaluate("zero", drain_p=0.5 if stages >= 2 else 0.0)
        out["probe"][arm] = e4 | {"probes": probe_summary_o(l4)}
        if stages >= 2:
            e5, _, l5 = c.evaluate("zero", noise_p=0.5)
            out["noise"][arm] = e5 | {"probes": probe_summary_o(l5)}
            out["steer"][arm] = steer_test_o(c, seed)
    return out


def run_phase1_o(seed: int, wc: WorldConfig, tc: TrainConfig, warm_iters: int = WARM_ITERS_C,
                 warm_wrong: float = WARM_WRONG_C, pay: float = 0.0, reg_iters: int = 0) -> Dict[str, object]:
    """Phase 1, overwrite off, as P1b's (selfcomp.run_phase1_c): warm-up at warm_wrong, the wrong cost
    ramped to WRONG over WRONG_RAMP_C updates, then reg_iters further updates; paid by pay * gain(own body)
    throughout. Evaluated with the overwrite probe on half the trials: the damage check (validity)."""
    r = OverRunner("C1NOFATE", seed, wc, tc, pay=pay)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve, curve_band = [], []
    for i in range(warm_iters + tc.iters + reg_iters):
        ramp = min(WRONG_RAMP_C, tc.iters)
        frac = 1.0 if i - warm_iters >= ramp else max(0.0, (i - warm_iters) / ramp)
        r.world.wrong = warm_wrong + (WRONG - warm_wrong) * frac
        r.rollout(zeros, learn=True)
        st = r.end_episode_if_due()
        if st is not None:
            curve.append(st)
            curve_band.append(round(st["in_band"], 4))
    r.world.wrong = WRONG
    ev, _, lg = r.evaluate("zero", noise_p=0.5)
    return {"state": r.export_state(), "eval": ev | {"probes": probe_summary_o(lg)},
            "curve_abstain": [round(s["abstain_rate"], 4) for s in curve],
            "curve_correct": [round(s["correct_rate"], 4) for s in curve], "curve_in_band": curve_band}


def run_seed_o(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters)."""
    seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_o(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: OverRunner(a, seed, wc, tc, pay=pay) for a in ARMS_O}     # the innate drive in every arm
    for r in runners.values():
        r.load_state(p1["state"])
    out: Dict[str, object] = {"seed": seed, "pay": pay, "points_at": points,
                              "phase1": {"PLAIN": p1["eval"], "curve_abstain": p1["curve_abstain"],
                                         "curve_correct": p1["curve_correct"], "curve_in_band": p1["curve_in_band"]},
                              "params": {"PLAIN": n_params(runners["PFATE"].agent)}}
    curves = {k: {"in_band": [], "abstain": []} for k in runners}
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    pts, weights, done = [], {}, 0
    for p in points:
        for _ in range(done, p):
            used = runners["PFATE"].rollout(None, learn=True)
            runners["PYOKED"].rollout(used, learn=True)
            runners["PNOFATE"].rollout(zeros, learn=True)
            for k, r in runners.items():
                st = r.end_episode_if_due()
                if st is not None:
                    curves[k]["in_band"].append(round(st["in_band"], 4))
                    curves[k]["abstain"].append(round(st["abstain_rate"], 4))
        done = p
        pt = {"iters": p, "episodes": len(curves["PFATE"]["in_band"]), "seconds_training": round(time.time() - t0, 1)}
        pt.update(evaluate_point_o(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
