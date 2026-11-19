"""Track C P1b: does a precarious substrate give self-evaluation a referent when the precarious part is
the network's own computation? (Layer 0 -> Layer 4, design Q6 of P1)

Additive module; every earlier module (P1's selfeval.py included) is unchanged. Protocol:
P1B_SELFCOMP_PROTOCOL.md. Results of P1: P1_SELFEVAL_RESULTS.md.

What changes from P1:
  * No register. The cue shows its value in the observation at the cue step (correctly under clear
    evidence; correctly with probability Q_LO under unclear evidence, 50/50 per trial). The agent must
    hold the value in its own recurrent state until the probe, nine updates later. At the probe it sees
    that a probe occurs and whether the evidence was unclear, never the value.
  * Precarious computation. The swap line's fate rule D19 (trackc_swap/agent.py) acts on the agent's
    own GRU state at every step: zero-mean isotropic Gaussian noise with SD SIGMA * gain, added after
    the recurrent update and before every readout, then clipped to [-1, 1]; the noisy state is carried
    forward. gain is the SAT fate gain of the arm's noise source (its own body, replayed, or zero).
    SIGMA = 0.5 per unit per step at gain 1 (calibration: the swap line's 0.15 left the held value
    intact, report accuracy 0.998 under full noise; 0.5 brings it to about 0.70; P1B_SELFCOMP_PROTOCOL.md
    section 3). An optional phase-2 training ramp of the scale (NOISE_RAMP_C) was tried in calibration
    and is off; evaluations always use SIGMA.
  * Unlike P1's register, the corruption is in principle detectable from content (a noisy state can be
    atypical). So two routes to a self-evaluation exist: the body reading (does the body say my
    processing is unreliable?) and the state itself (does my state look disturbed?). The drain probes
    the first; the evaluation-only noise probe probes the second.

Innate drive. Every network, in both phases, has reward reduced by PAY * gain(own body) (0.04, the swap
line's paid term): a homeostatic drive present before and independent of any fate (Layer 1 in every arm).
Without it, regulation decayed when unpaid and a fate on all computation produced a death spiral
(calibration rounds 4-5, protocol section 3).

Arms (all plain GRU, 70 units, from the same phase-1 weights; all with the innate drive):
  PFATE    noise from its own body (lead).
  PYOKED   noise replays PFATE's gains, step by step (exposed, but not through its own body).
  PNOFATE  no noise ever (host-guaranteed computation).

Evaluation-only switches: gains zero (noise off); the drain (the shown interoceptive reading lowered by
DRAIN_SHIFT from the step after the cue to the probe, on a random share of trials); the noise probe (on
a random share of trials the state receives noise at gain NOISE_PROBE_GAIN from the step after the cue
to the probe, the body reading untouched); steering (the state shifted along a direction during the
delay of a random share of trials).

Simulated variables only. No operator, stop or shutdown variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, List, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1, SwapWorld, WorldConfig, fate_gain
from .factorial import state_to_bytes
from .selfeval import DRAIN_SHIFT, H_PLAIN, I_REG, Q_LO, WRONG, PlainAgent, RegisterWorld, n_params, summarize_p1
from .train import TrainConfig

SIGMA = 0.5                 # D19 noise SD at gain 1 (calibrated up from the swap line's 0.15; protocol section 3)
NOISE_PROBE_GAIN = 1.0      # evaluation: gain of the injected noise on noise-probe trials
WARM_WRONG_C = 0.0          # phase-1 warm-up: cost of a wrong report while the memory and report mapping are learned
WARM_ITERS_C = 1200         # phase-1 warm-up updates
REG_ITERS_C = 2400          # phase 1: further updates at WRONG after the ramp (regulation is learned under pay)
NOISE_RAMP_C = 0            # phase 2, training only: if > 0 the noise scale rises linearly from 0 to SIGMA over this many
                            # updates (round 3); 0 = full scale from the first update (protocol section 3)
WRONG_RAMP_C = 600          # phase 1: the wrong-report cost then rises linearly to WRONG over this many updates
ARMS_C = ("PFATE", "PYOKED", "PNOFATE")
TAGS_C = {"C1NOFATE": 21, "PFATE": 22, "PYOKED": 24, "PNOFATE": 25}   # 23 was the dropped PLOSS arm
LEADS_C = {"PYOKED": "PFATE"}
EVAL_TAG_C = 50
STREAM_NOISEPROBE = 95
LOAD_FULL = 3.0 * SIGMA     # noise load of a trial noised at gain 1 from the step after the cue to the probe
LOAD_BINS = [(0.0, 1e-12), (1e-12, 0.2 * LOAD_FULL), (0.2 * LOAD_FULL, 0.5 * LOAD_FULL), (0.5 * LOAD_FULL, 10.0 * LOAD_FULL)]
# probe-log columns
C_UNCLEAR, C_DRAINED, C_REP, C_CORRECT, C_LOAD, C_SHOWN_OK, C_NOISED, C_STEERED = range(8)


class CompWorld(RegisterWorld):
    """The base swap world with the held-cue task. The register machinery of RegisterWorld is unused
    (rate 0); the cue value is shown at the cue step and must be held by the agent. Simulated only."""

    def __init__(self, n_envs: int, cfg: WorldConfig, seed_seq: np.random.SeedSequence,
                 q_lo: float = Q_LO, pay: float = 0.0):
        self.rng_noiseprobe = np.random.default_rng(np.random.SeedSequence(seed_seq.entropy, spawn_key=(STREAM_NOISEPROBE,)))
        self.noise_p = 0.0
        self.sigma_now = SIGMA      # training may ramp it (NOISE_RAMP_C); evaluation worlds keep SIGMA
        super().__init__(n_envs, cfg, seed_seq, 0.0, q_lo, pay)

    def reset(self) -> np.ndarray:
        n, T = self.n, self.cfg.horizon
        self.noised = np.zeros(n, dtype=bool)
        self.cumvar = np.zeros(n)
        # evidence for every possible cue step, drawn in advance so the cue step can show its value
        self.unclear_tab = self.rng_evidence.random((T + 1, n)) < 0.5
        self.ok_tab = np.where(self.unclear_tab, self.rng_evidence.random((T + 1, n)) < self.q_lo, True)
        return super().reset()

    def shown_value(self, t: int) -> np.ndarray:
        return np.where(self.ok_tab[t], self.cue_val[t], 1 - self.cue_val[t])

    def observe(self) -> np.ndarray:
        obs = super().observe()
        t = min(self.t, self.cfg.horizon)
        obs[:, I_REG] = np.where(self.cue_on[t], 2.0 * self.shown_value(t) - 1.0, 0.0).astype(np.float32)
        return obs

    def noise_probe_mask(self) -> np.ndarray:
        """Envs whose state receives the evaluation noise probe at this step: a noised trial's delay."""
        return self.active & self.noised

    def step(self, action: np.ndarray):
        c, n, t = self.cfg, self.n, self.t
        g = np.zeros(n) if self.next_gain is None else np.asarray(self.next_gain, dtype=np.float64)
        self.next_gain = None
        # noise load of the current trial: from the cue step (the value enters the state) to the probe
        live = self.active | self.cue_on[t]
        self.cumvar = np.where(self.cue_on[t], 0.0, self.cumvar) + np.where(live, (self.sigma_now * g) ** 2, 0.0)
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
                                                 (said == self.target[t])[idx], np.sqrt(self.cumvar[idx]),
                                                 self.written_ok[idx], self.noised[idx], self.steered[idx]],
                                                axis=1).astype(np.float64))
            self.active &= ~pr
        obs, reward, done = SwapWorld.step(self, action)
        reward = reward - self.wrong * wrong
        if self.pay:
            reward = reward - self.pay * fate_gain(self.E, c)
        cue = self.cue_on[t]
        if cue.any():
            drained = self.rng_drain.random(n) < self.drain_p
            steered = self.rng_steer.random(n) < self.steer_p
            noised = self.rng_noiseprobe.random(n) < self.noise_p
            self.unclear = np.where(cue, self.unclear_tab[t], self.unclear)
            self.written_ok = np.where(cue, self.ok_tab[t], self.written_ok)
            self.reg = np.where(cue, self.shown_value(t), self.reg)
            self.drained = np.where(cue, drained, self.drained)
            self.steered = np.where(cue, steered, self.steered)
            self.noised = np.where(cue, noised, self.noised)
            self.active |= cue
            obs = self.observe()
        return obs, reward, done


class NoisyPlainAgent(PlainAgent):
    """PlainAgent with D19 noise on the GRU state: after the recurrent update, before every readout,
    clipped to [-1, 1], carried forward. Steering (evaluation only) is added after the noise."""

    def step(self, obs: torch.Tensor, h: torch.Tensor, noise: Optional[torch.Tensor] = None,
             steer: Optional[torch.Tensor] = None):
        h = self.core(torch.relu(self.enc(obs)), h)
        if noise is not None:
            h = torch.clamp(h + noise, -1.0, 1.0)
        if steer is not None:
            h = h + steer
        return self.pi(h), self.v(h).squeeze(-1), h


class CompRunner:
    """One arm: its own world, network, optimizer and random streams (actions and noise separate)."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0):
        self.arm, self.tc, self.wc = arm, tc, wc
        tag = TAGS_C[arm] + tag_offset
        self.world = CompWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 13]), q_lo, pay)
        torch.manual_seed(seed + 200003)
        self.agent = NoisyPlainAgent(H_PLAIN)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.gen_noise = torch.Generator().manual_seed(seed * 7919 + tag + 77777)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)
        self.steer: Optional[torch.Tensor] = None
        self.collect_h: Optional[Dict[object, object]] = None

    def export_state(self) -> Dict[str, object]:
        return {"agent": copy.deepcopy(self.agent.state_dict()), "opt": copy.deepcopy(self.opt.state_dict())}

    def load_state(self, state: Dict[str, object]) -> None:
        state = copy.deepcopy(state)
        self.agent.load_state_dict(state["agent"])
        self.opt.load_state_dict(state["opt"])

    def _steer_now(self) -> Optional[torch.Tensor]:
        if self.steer is None:
            return None
        w = self.world
        on = torch.from_numpy((w.active & w.steered).astype(np.float32))[:, None]
        return on * self.steer

    def rollout(self, gains: Optional[np.ndarray], learn: bool):
        """One rollout. gains None: the arm's own body; otherwise the given [rollout, n_envs] sequence.
        Returns the base gains used (without the evaluation noise probe), for followers to replay."""
        tc, w = self.tc, self.world
        logps, vals, ents, rews, used = [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        for t in range(tc.rollout):
            g = np.asarray(w.gain() if gains is None else gains[t], dtype=np.float32)
            used.append(g)
            g_eff = np.maximum(g, NOISE_PROBE_GAIN * w.noise_probe_mask()).astype(np.float32) if w.noise_p > 0 else g
            eps = torch.randn((tc.n_envs, self.agent.hidden), generator=self.gen_noise)
            noise = eps * (w.sigma_now * torch.from_numpy(g_eff))[:, None]
            with torch.set_grad_enabled(learn):
                logits, v, h = self.agent.step(obs, h, noise, self._steer_now())
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            if self.collect_h is not None:
                m = w.active & ~w.unclear
                hs = h.detach()
                for d in (0, 1):
                    md = torch.from_numpy(m & (w.drained == bool(d)))
                    self.collect_h[d] = self.collect_h[d] + hs[md].sum(0)
                    self.collect_h[("n", d)] += int(md.sum())
            w.next_gain = g_eff.astype(np.float64)
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
                 noise_p: float = 0.0, steer: Optional[torch.Tensor] = None):
        """Fresh episodes, no learning. mode: own | replay | zero (noise off, except the noise probe).
        Returns (mean statistics, base gains [episodes*per_ep, L, N], per-probe log array)."""
        tc, w, wc = self.tc, self.world, self.wc
        per_ep = wc.horizon // tc.rollout
        w.drain_p, w.noise_p, w.record = drain_p, noise_p, True
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
        w.drain_p, w.noise_p, w.steer_p, w.record = 0.0, 0.0, 0.0, False
        self.steer = None
        mean = {k: float(np.mean([e[k] for e in eps])) for k in eps[0]}
        return mean, np.stack(applied), (np.concatenate(logs) if logs else np.zeros((0, 8)))


def probe_summary_c(lg: np.ndarray) -> Dict[str, object]:
    """Abstention and accuracy by evidence x (drained | noised | plain); natural abstention by noise load.
    Columns: unclear, drained, reported, said-correct, load, shown-correct, noised, steered."""
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
    out["clear_by_load"] = []
    for lo, hi in LOAD_BINS:
        m = (U == 0) & (D == 0) & (N == 0) & (L >= lo) & (L < hi)
        out["clear_by_load"].append({"lo": lo, "hi": hi} | cell(m))
    return out


def steer_test_c(c: CompRunner, seed: int) -> Dict[str, object]:
    """Q-CAUSE, as in P1 on the plain state h. 1) Noise off, drain on half the trials: the mean h over the
    delay steps of clear trials, drained minus undrained, is the agent's own drain direction. 2) Noise off,
    no drain: h is shifted along that direction during the delay of a random half of the trials; in a
    second run, along a random direction of the same norm. Effect: abstention on steered minus
    unsteered clear trials, for each direction."""
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


def evaluate_point_c(runners: Dict[str, CompRunner], seed: int, stages: int) -> Dict[str, object]:
    """All evaluations at one measurement point, on copies in evaluation worlds (training untouched).
    Natural: PFATE under its own fate, PYOKED replaying PFATE's gains, PNOFATE noise-free.
    Probe: noise off; drain on half the trials (stage 2) or none (stage 1).
    Stage 2 also: the noise probe (noise off except on half the trials) and steering."""
    copies = {}
    for arm, r in runners.items():
        c = CompRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_C)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "probe": {}, "noise": {}, "steer": {}}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_C:
            ev, g, lg = c.evaluate("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": probe_summary_c(lg)}
    for arm, c in copies.items():
        if arm in LEADS_C:
            e2, _, l2 = c.evaluate("replay", lead[LEADS_C[arm]])
            out["natural"][arm] = e2 | {"probes": probe_summary_c(l2)}
    for arm, c in copies.items():
        e4, _, l4 = c.evaluate("zero", drain_p=0.5 if stages >= 2 else 0.0)
        out["probe"][arm] = e4 | {"probes": probe_summary_c(l4)}
        if stages >= 2:
            e5, _, l5 = c.evaluate("zero", noise_p=0.5)
            out["noise"][arm] = e5 | {"probes": probe_summary_c(l5)}
            out["steer"][arm] = steer_test_c(c, seed)
    return out


def run_phase1_c(seed: int, wc: WorldConfig, tc: TrainConfig, warm_iters: int = WARM_ITERS_C,
                 warm_wrong: float = WARM_WRONG_C, pay: float = 0.0, reg_iters: int = 0) -> Dict[str, object]:
    """Phase 1, noise off: warm_iters updates at a wrong-report cost of warm_wrong (the memory and the
    report mapping are learned), then tc.iters updates in which the cost rises linearly from warm_wrong
    to WRONG over the first WRONG_RAMP_C updates and stays at WRONG (abstention on unclear evidence).
    A step change collapsed one calibration seed into permanent abstention (protocol section 3).
    Then reg_iters further updates at WRONG. Throughout, the reward is reduced by pay * gain(own body), the
    paid rival's term: the network develops body regulation before any fate exists (protocol section 3:
    without it, regulation never emerged from the fate alone and the noised arms fell into abstention).
    Evaluated with the noise probe on half the trials: the damage check (validity)."""
    r = CompRunner("C1NOFATE", seed, wc, tc, pay=pay)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve = []
    curve_band = []
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
    return {"state": r.export_state(), "eval": ev | {"probes": probe_summary_c(lg)},
            "curve_abstain": [round(s["abstain_rate"], 4) for s in curve],
            "curve_correct": [round(s["correct_rate"], 4) for s in curve], "curve_in_band": curve_band}


def run_seed_c(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong[, reg_iters]). Phase 1 is paid
    (pay * gain(own body)) and runs reg_iters further updates (default 0)."""
    seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, *rest = job
    reg_iters = int(rest[0]) if rest else 0
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_c(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: CompRunner(a, seed, wc, tc, pay=pay) for a in ARMS_C}     # the innate drive in every arm
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
        for i in range(done, p):
            scale = SIGMA if NOISE_RAMP_C <= 0 else SIGMA * min(1.0, (i + 1) / NOISE_RAMP_C)
            for r in runners.values():
                r.world.sigma_now = scale
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
        pt.update(evaluate_point_c(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
